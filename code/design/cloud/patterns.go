package main

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"
)

type Circuit func(context context.Context, workflow string) error

var ErrServiceUnavailable = errors.New("service unreachable")

/*
Circuit Breaker automatically degrades service functions in response to a likely fault,
preventing larger or cascading failures by eliminating recurring errors and providing
reasonable error responses
*/
func Breaker(circuit Circuit, failureThreshold uint) Circuit {

	var consecutiveFailures int
	var lastAttempt = time.Now()
	var m sync.RWMutex

	return func(ctx context.Context, workflow string) error {
		
		m.Lock()
		defer m.Unlock()

		d := consecutiveFailures - int(failureThreshold)
		fmt.Printf("consec fail: %v for %d", consecutiveFailures, d)
		if d >= 0 {
			shouldRetryAt := lastAttempt.Add(time.Second * 2 << 2)
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


func FaultyBreaker(circuit Circuit, failureThreshold uint) Circuit {

	/* Faulty: because the lock release and acquisition, goroutines can execute the circuit, overwhelming the service 
	TODO: will test this
	*/

	var consecutiveFailures int
	var lastAttempt = time.Now()
	var m sync.RWMutex

	return func(ctx context.Context, workflow string) error {
		m.RLock()

		d := consecutiveFailures - int(failureThreshold)
		fmt.Printf("consec fail: %v for %d", consecutiveFailures, d)
		if d >= 0 {
			shouldRetryAt := lastAttempt.Add(time.Second * 2 << 2)
			if !time.Now().After(shouldRetryAt) {
				m.RUnlock()
				return ErrServiceUnavailable
			}
		}

		m.RUnlock()

		m.Lock()
		defer m.Unlock()

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