package main

import (
	"context"
	"errors"
	"sync"
	"time"
)

type Circuit func(context context.Context) (string, error)

/*
Circuit Breaker automatically degrades service functions in response to a likely fault,
preventing larger or cascading failures by eliminating recurring errors and providing
reasonable error responses
*/
func Breaker(circuit Circuit, failureThreshold uint) Circuit {

	var consecutiveFailures int
	var lastAttempt = time.Now()
	var m sync.RWMutex

	return func(ctx context.Context) (string, error) {
		m.RLock()

		d := consecutiveFailures - int(failureThreshold)

		if d >= 0 {
			shouldRetryAt := lastAttempt.Add(time.Second * 2 << 2)
			if !time.Now().After(shouldRetryAt) {
				m.RUnlock()
				return "", errors.New("service unreachable")
			}
		}

		m.RUnlock()

		m.Lock()
		defer m.Unlock()

		response, err := circuit(ctx)

		lastAttempt = time.Now()

		if err != nil {
			consecutiveFailures++
			return response, err
		}

		consecutiveFailures = 0

		return response, nil
	}

}