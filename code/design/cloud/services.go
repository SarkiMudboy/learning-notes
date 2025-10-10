package main

import (
	"context"
	"errors"
	"sync"
)

var ErrServiceFailure = errors.New("Service Failure")

func ForCircuitBreaker() Circuit {

	var runs int
	var r sync.RWMutex

	return func(context context.Context, workflow string) (error) {
		
		var response error
		
		r.Lock()

		switch workflow {
		case "consecutive failures":
			response = ErrServiceFailure
		case "intermediate failures":
			if runs % 2 == 0 {
				response = ErrServiceFailure
			}
		case "normal":
		}

		runs++

		defer r.Unlock()

		return response
	}

}