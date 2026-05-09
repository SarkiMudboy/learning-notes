package main

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"
)

const ServiceResponse = "Attention Is All You Need"

var ErrServiceFailure = errors.New("service failure")
var ErrTooManyRequests = errors.New("too many requests")
var ErrInvalidInput = errors.New("invalid input")

type Tracker struct {
	update uint
	delay  time.Time
	err    error
	l      sync.Mutex
}

func ForCircuitBreaker() BreakerCircuit {

	var runs int
	var r sync.RWMutex

	return func(ctx context.Context, workflow string) error {

		var response error

		r.Lock()

		switch workflow {
		case "consecutive failures":
			response = ErrServiceFailure
		case "intermediate failures":
			if runs%2 != 0 {
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

func ForRetry() Effector {

	var calls int
	var r sync.Mutex
	const secretPhrase = "I AM THE ONE"

	return func(ctx context.Context) (string, error) {

		r.Lock()
		defer r.Unlock()

		calls++

		if calls > 3 {
			return secretPhrase, nil
		}
		return "", ErrServiceFailure
	}
}

func ForThrottle() Effector {
	const Length = 40
	var r sync.RWMutex
	results := []string{}

	for range Length {
		results = append(results, "099")
	}

	return func(ctx context.Context) (string, error) {
		r.RLock()
		defer r.RUnlock()

		if len(results) == 0 {
			return "", ErrServiceFailure
		}

		result := results[len(results)-1]
		return result, nil
	}
}

func ForTimeout(d int) (string, error) {
	// simple slow function
	const ErrorThreshold = 10

	if d > ErrorThreshold {
		return "", ErrServiceFailure
	}

	time.Sleep(time.Second * time.Duration(d))
	return ServiceResponse, nil
}

// concurrency
func ForFanIn(numOfSources int, numOfValues int) []int {
	sources := make([]<-chan int, numOfSources)
	var results []int

	for i := 0; i < numOfSources; i++ {
		ch := make(chan int)
		// fmt.Printf("Here %d", i)
		sources[i] = ch

		go func() {
			defer close(ch)
			for j := 0; j < numOfValues; j++ {
				ch <- j
				time.Sleep(time.Second * 2)
			}
		}()
	}
	out := Funnel(sources...)
	for s := range out {
		results = append(results, s)
	}
	return results
}

func ForFanOut(batchSize int, value int) (int, error) {

	if value % batchSize != 0 {
		return 0, ErrInvalidInput
	}

	outSize := value / batchSize
	source := make(chan int)
	result := make(chan int)
	
	dests := Split(source, outSize)
	
	var wg sync.WaitGroup 
	factorial := 1
	
	go func() {
		for i := 1; i <= value; i++ {
			source <- i
		}
		close(source)
	}()

	wg.Add(len(dests))

	for i, d := range dests {
		go func(i int, ch <-chan int) {
			defer wg.Done()
			total := 1

			// continously loop through the channel and compute product
			for v := range d{
				total *= v
			}
			
			fmt.Printf("recieved total -> %d\n", total)
			result <- total

		}(i, d)
	}
	
	go func() {
		wg.Wait()
		close(result)
	}()

	for r := range result{
		factorial *= r
	}
	
	return factorial, nil
}

func ForFanOutRoundRobin(batchSize int, value int) (int, error) {

	if value % batchSize != 0 {
		return 0, ErrInvalidInput
	}

	outSize := value / batchSize
	source := make(chan int)	
	dests := Split(source, outSize)
	
	factorial := 1
	
	go func() {
		for i := 1; i <= value; i++ {
			source <- i
		}
		close(source)
	}()

	current := 0

	for {
		index := current % len(dests)
		dest := dests[index]
		val, ok := <- dest
		if !ok {
			break
		}
		fmt.Printf("obtained: %v from %d\n", val, index)
		factorial *= val
		current++
	}
	
	return factorial, nil
}



func ForFuture(ctx context.Context, delayInSecs uint, result string) Future {
	resCh := make(chan string)
	errChan := make(chan error)

	go func() {
		select {
			case <- time.After(time.Second * time.Duration(delayInSecs)):
				resCh <- result
				errChan <- nil
			case <- ctx.Done():
				resCh <- ""
				errChan <- ctx.Err()
		}
	}()
	
	return NewInnerFuture(resCh, errChan)
}
