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

func DebounceFirst (c DebouceCircuit, d time.Duration) DebouceCircuit {
	
	var threshold time.Time
	var result int
	var err error
	var m sync.Mutex

	return func(ctx context.Context) (int, error) {

		m.Lock()

		defer func(){
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

func DebounceLast (c DebounceLastCircuit, d time.Duration) DebounceLastCircuit {

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
					case <- ticker.C:
						m.Lock()
						if time.Now().After(threshold) {
							fmt.Println("tick")
							result, err = c(ctx, t)
							m.Unlock()
							return
						}
						m.Unlock()
					case <- ctx.Done():
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