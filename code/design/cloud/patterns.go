package main

import (
	"context"
	"errors"
	"sync"
	"time"
)

type BreakerCircuit func(context context.Context, workflow string) error

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

		if err != nil {
			consecutiveFailures++
			return err
		}

		consecutiveFailures = 0

		return nil
	}

}

type DebouceCircuit func(ctx context.Context) (int, error) 

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
		// fmt.Println(result)

		return result, err
	}
}