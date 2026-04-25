package main

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"
)

type BreakerCircuit func(context context.Context, workflow string) error
type DebouceCircuit func(ctx context.Context) (int, error)
type DebounceLastCircuit func(ctx context.Context, t *Tracker) (int, error)
type Effector func(ctx context.Context) (string, error)
type SlowFunction func(d int) (string, error)

var ErrServiceUnavailable = errors.New("service unreachable")

/*
Circuit Breaker automatically degrades service functions in response to a likely fault,
preventing larger or cascading failures by eliminating recurring errors and providing
reasonable error responses
*/
func Breaker(circuit BreakerCircuit, failureThreshold uint) BreakerCircuit {

	var consecutiveFailures int
	var lastAttempt = time.Now()
	var m sync.RWMutex

	return func(ctx context.Context, workflow string) error {

		m.Lock()
		defer m.Unlock()

		d := consecutiveFailures - int(failureThreshold)

		if d >= 0 {
			shouldRetryAt := lastAttempt.Add(time.Second * 2 << d)
			if !time.Now().After(shouldRetryAt) {
				return ErrServiceUnavailable
			}
		}

		err := circuit(ctx, workflow)

		lastAttempt = time.Now()

		if err != nil {
			consecutiveFailures++
			return err
		}

		consecutiveFailures = 0
		return nil
	}

}

func FaultyBreaker(circuit BreakerCircuit, failureThreshold uint) BreakerCircuit {

	/* Faulty: because the lock release and acquisition, goroutines can execute the circuit, overwhelming the service
	TODO: will test this
	*/

	var consecutiveFailures int
	var lastAttempt = time.Now()
	var m sync.RWMutex

	return func(ctx context.Context, workflow string) error {
		m.RLock()

		d := consecutiveFailures - int(failureThreshold)

		if d >= 0 {

			shouldRetryAt := lastAttempt.Add(time.Second * 2 << d)
			if !time.Now().After(shouldRetryAt) {
				m.RUnlock()
				return ErrServiceUnavailable
			}
		}

		m.RUnlock()

		err := circuit(ctx, workflow)

		m.Lock()
		defer m.Unlock()

		lastAttempt = time.Now()
		fmt.Println(consecutiveFailures)
		if err != nil {
			consecutiveFailures++
			return err
		}

		consecutiveFailures = 0

		return nil
	}

}

func DebounceFirst(c DebouceCircuit, d time.Duration) DebouceCircuit {

	var threshold time.Time
	var result int
	var err error
	var m sync.Mutex

	return func(ctx context.Context) (int, error) {

		m.Lock()

		defer func() {
			threshold = time.Now().Add(d)
			m.Unlock()
		}()

		if time.Now().Before(threshold) {
			return result, err
		}

		result, err = c(ctx)

		return result, err
	}
}

func DebounceLast(c DebounceLastCircuit, d time.Duration) DebounceLastCircuit {

	var m sync.Mutex
	var err error
	var result int
	var threshold time.Time
	var once sync.Once

	return func(ctx context.Context, t *Tracker) (int, error) {

		m.Lock()
		defer m.Unlock()

		threshold = time.Now().Add(d)

		once.Do(func() {
			ticker := time.NewTicker(time.Millisecond * 100)
			go func() {
				defer func() {
					m.Lock()
					ticker.Stop()
					once = sync.Once{}
					m.Unlock()
				}()

				for {
					select {
					case <-ticker.C:
						m.Lock()
						if time.Now().After(threshold) {
							fmt.Println("tick")
							result, err = c(ctx, t)
							m.Unlock()
							return
						}
						m.Unlock()
					case <-ctx.Done():
						m.Lock()
						result, err = 0, ctx.Err()
						m.Unlock()
						return
					}
				}
			}()
		})
		return result, err
	}
}

func Retry(e Effector, retries int, delay time.Duration) Effector {
	return func(ctx context.Context) (string, error) {
		for r := 0; ; r++ {
			response, err := e(ctx)

			if err == nil || r > retries {
				return response, err
			}

			fmt.Printf("Attempt %d failed, retrying in %v\n", r+1, delay)

			select {
			case <-time.After(delay):
			case <-ctx.Done():
				return "", ctx.Err()
			}
		}
	}
}

/*
 Throttle limits the frequency of a function call to some maximum number of invoca‐
 tions per unit of time.
*/

func Throttle(e Effector, max uint, refill uint, d time.Duration) Effector {
	var tokens = max
	var once sync.Once

	return func(ctx context.Context) (string, error) {
		if ctx.Err() != nil {
			return "", ctx.Err()
		}

		once.Do(func() {
			ticker := time.NewTicker(d)

			go func() {
				for {
					defer ticker.Stop()
					select {
					case <-ctx.Done():
						return
					case <-ticker.C:
						t := tokens + refill
						if t > max {
							t = max
						}
						tokens = t
					}
				}
			}()
		})
		// fmt.Println(tokens)
		if tokens <= 0 {
			return "", ErrTooManyRequests
		}

		tokens--
		return e(ctx)
	}
}

/*
* Timeout allows a process to stop waiting for an answer once it’s clear that an answer
may not be coming.
*/
func Timeout(f SlowFunction, t time.Duration) (SlowFunction, context.CancelFunc) {
	ctx := context.Background()
	tctx, cancel := context.WithTimeout(ctx, t)
	var m sync.RWMutex

	sf := func(d int) (string, error) {

		m.RLock()
		defer m.RUnlock()

		cherr := make(chan error)
		chres := make(chan string)

		go func() {
			res, err := f(d)
			chres <- res
			cherr <- err
		}()

		select {
		case res := <-chres:
			return res, <-cherr
		case <-tctx.Done():
			return "", tctx.Err()
		}
	}

	return sf, cancel
}
