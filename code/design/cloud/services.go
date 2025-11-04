package main

import (
	"context"
	"errors"
	"sync"
	"time"
)

var ErrServiceFailure = errors.New("service failure")
var ErrTooManyRequests = errors.New("too many requests")

func ForCircuitBreaker() BreakerCircuit {

	var runs int
	var r sync.RWMutex

	return func(ctx context.Context, workflow string) (error) {
		
		var response error
		
		r.Lock()

		switch workflow {
		case "consecutive failures":
			response = ErrServiceFailure
		case "intermediate failures":
			if runs % 2 != 0 {
				response = ErrServiceFailure
			} else {
				response = nil
			}
		default:
		}

		runs++

		defer r.Unlock()

		return response
	}

}

func ForDebounce() DebouceCircuit {
	var runs int
	var r sync.Mutex
	var err error

	return func(ctx context.Context) (int, error) {
		
		r.Lock()
		defer r.Unlock()
		
		if runs >= 1 {
			return runs, ErrTooManyRequests
		}
	
		runs++
		return runs, err
	}
}

func ForDebounceLast() DebounceLastCircuit {
	var runs int
	var r sync.Mutex
	var err error

	return func(ctx context.Context, resChan chan time.Time, errChan chan error) (int, error) {
		
		r.Lock()
		defer r.Unlock()

		if runs >= 1 {

			e := ErrTooManyRequests
			
			resChan <- time.Now()
			errChan <- e

			return runs, e
		}

		runs++
		resChan <- time.Now()
		return runs, err
	}
}