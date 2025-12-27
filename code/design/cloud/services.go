package main

import (
	"context"
	"errors"
	"sync"
	"time"
)

var ErrServiceFailure = errors.New("service failure")
var ErrTooManyRequests = errors.New("too many requests")


type Tracker struct {
	update uint
	delay time.Time
	err error
	l sync.Mutex
}

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

	return func(ctx context.Context, t *Tracker) (int, error) {
		
		r.Lock()
		defer r.Unlock()

		t.l.Lock()
		defer t.l.Unlock()

		if runs >= 1 {
			e := ErrTooManyRequests
			t.delay = time.Now()
			t.err = e
			return runs, e
		}

		runs++

		t.update = uint(runs)
		t.delay = time.Now()
		
		return runs, err
	}
}