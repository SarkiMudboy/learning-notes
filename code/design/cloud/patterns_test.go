package main

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"testing"
	"time"
)

const checkMark = "\u2713"
const ballotX = "\u2717"

func TestCircuitBreaker(t *testing.T) {

	service := Breaker(ForCircuitBreaker(), 2)

	t.Log("Given the need to test that Circuit Breaker can invoke and return values upon a successful request")
	{
		t.Log("When calling the `ForCircuitBreaker Wrapper function` with default context value")
		{
			err := service(context.Background(), "normal")
			if err != nil {
				t.Fatalf("Should pass as initial service run is successful: %v", ballotX)
			}
			t.Logf("Should pass as initial service run is successful: %v", checkMark)
		}
	}
}


func TestBreakerStayClosed(t *testing.T) {
	service := Breaker(ForCircuitBreaker(), 4)
	errChan := make(chan error, 6)
	ctx := context.Background()

	t.Log("Given the need to test that the Circuit stay closed when failure threshold has not been reached")
	{
		t.Log("When calling the `ForCircuitBreaker Wrapper function` as 4 goroutines with default context value")
		{
			for j := 0; j <= 10; j++ {
				go func() {
					e := service(ctx, "consecutive failures")
					errChan <- e
				}()
			}

			for j := 0; j <= 10; j++ {
				select {
					case err := <- errChan:
						fmt.Println(err)
						if !errors.Is(ErrServiceFailure, err) {
							t.Errorf("Should return only Service Failure errors as Breaker threshold limit has not being hit: %v", ballotX)
						}
					case <- ctx.Done():
						t.Fatal("Error: could not complete test")
				}
			}
			
			t.Logf("Should return only Service Failure errors as Breaker threshold limit has not being hit: %v", checkMark)
		}
	}
	
}

func TestBreakerIntermediateFailures(t *testing.T) {
	service := Breaker(ForCircuitBreaker(), 4)
	errChan := make(chan error, 6)
	ctx := context.Background()
	runs := 14
	var expErr error

	t.Log("Given the need to test that the Circuit stays closed when intermediate failures occurs")
	{
		t.Logf("When calling the `ForCircuitBreaker Wrapper function` with default context value as %d goroutines", runs)
		{
			for j := 0; j <= runs; j++ {
				go func() {
					e := service(ctx, "intermediate failures")
					errChan <- e
				}()
			}

			for j := 0; j <= runs; j++ {
				select {
					case err := <- errChan:
						expErr = err
						t.Log(err)
					case <- ctx.Done():
						t.Fatal("Error: could not complete test")
				}
			}
		}

		if expErr != nil {
			t.Fatalf("Should not return errors as the last Circuit execution was successful: %v", ballotX)
		}
		t.Logf("Should not return errors as the last Circuit execution was successful: %v", checkMark)
	}
}

func TestBreakerTrips(t *testing.T) {
	service := FaultyBreaker(ForCircuitBreaker(), 4)
	errChan := make(chan error, 30)
	ctx := context.Background()
	runs := 30
	var expErr error


	t.Log("Given the need to test that the Circuit opens when failure threshold has been reached")
	{
		t.Logf("When calling the `ForCircuitBreaker Wrapper function` with default context value as %d goroutines", runs)
		{
			for j := 0; j <= runs; j++ {
				go func() {
					e := service(ctx, "consecutive failures")
					errChan <- e
				}()
			}

			for j := 0; j <= runs; j++ {
				select {
					case err := <- errChan:
						expErr = err
					case <- ctx.Done():
						t.Fatal("Error: could not complete test")
				}
			}

			if !errors.Is(ErrServiceUnavailable, expErr) {
				t.Fatalf("Should return Service Unavailable errors as Breaker threshold limit has being hit: %v", ballotX)
			}
			t.Logf("Should return Service Unavailable errors as Breaker threshold limit has being hit: %v", checkMark)
		}
	}
	
}

func TestDebounceLimitRequests(t *testing.T) {

	var serviceRuns int
	var expErr error
	service := DebounceFirst(ForDebounce(), time.Millisecond*2)
	runs := 10
	resultChan := make(chan int)
	errChan := make(chan error)
	ctx := context.Background()

	t.Logf("Given the need to test that the requests cluster of %d are debounced", runs)
	{
		t.Logf("When calling the `ForDebounce` Wrapper function` with default context value as %d goroutines", runs)
		{
			for j := 0; j <= runs; j++ {
				go func() {
					r, err := service(ctx)
					resultChan <- r
					errChan <- err
				}()
			}

			for j := 0; j <= runs; j++ {
				select {
					case run := <- resultChan:
						serviceRuns = run
						fmt.Println(run)
					case err := <- errChan:
						expErr = err
						fmt.Println(err)
					case <- ctx.Done():
						t.Fatal("Error: could not complete test")
				}
			}

			if errors.Is(ErrTooManyRequests, expErr) {
				t.Fatalf("Should not return too many request error as the cluster of requests should have debounced: %v", ballotX)
			}
			t.Logf("Should not return too many request error as the cluster of requests should have debounced: %v", checkMark)

			if serviceRuns > 1 {
				t.Fatalf("the service should only run once, the first operation in the cluster %v", ballotX)
			}
			t.Logf("the service should only run once, the first operation in the cluster %v", checkMark)
		}
	}
}

func TestDebounceLastExecutesOnlyOnce(t *testing.T) {

	var tr Tracker
	var wg sync.WaitGroup
	service := DebounceLast(ForDebounceLast(), time.Millisecond*500)
	runs := 10
	wg.Add(runs)
	ctx := context.Background()
	

	t.Logf("Given the need to test that the last request in a cluster of %d requests executes only once after the debounce duration", runs)
	{
		t.Logf("When calling the `ForDebounce` Wrapper function` with default context value as %d goroutines", runs)
		{
			for j := 0; j < runs; j++ {
				go func() {
					_, _ = service(ctx, &tr)
					wg.Done()
				}()
			}
			
			wg.Wait()

			if errors.Is(ErrTooManyRequests, tr.err) {
				t.Fatalf("Should not return too many request error as the last request should have executed after debounce duration: %v", ballotX)
			}
			t.Logf("Should not return too many request error as the last request should have executed after debounce duration: %v", checkMark)

			if tr.update != 1 {
				t.Fatalf("the service should only run once, the last operation in the cluster %v", ballotX)
			}
			t.Logf("the service should only run once, the last operation in the cluster %v", checkMark)
		}
	}

}

func TestDebounceLastExecutesLast(t *testing.T) {
	var delay time.Time
	var start time.Time
	var expErr error
	// service := DebounceLast(ForDebounceLast(), time.Millisecond*500)
	runs := 10
	resultChan := make(chan time.Time)
	errChan := make(chan error)
	ctx := context.Background()

	t.Logf("Given the need to test that the last request in a cluster of %d requests executes only once after the debounce duration", runs)
	{
		t.Logf("When calling the `ForDebounce` Wrapper function` with default context value as %d goroutines", runs)
		{

			start = time.Now()
			for j := 0; j < runs; j++ {
				go func() {
					// service(ctx, resultChan, errChan)
					fmt.Print("ddd")
				}()
			}

			// for {
			select {
				case delay = <- resultChan:
					fmt.Printf("service run at: %v\n", delay)
					if delay.Before(start.Add(time.Millisecond * 500)) {
						t.Fatalf("the service should only run once, the last operation in the cluster %v", ballotX)
					} 
				case expErr = <- errChan:
					fmt.Printf("error: %v\n", expErr)
				case <- ctx.Done():
					t.Fatal("Error: could not complete test")
			}
			
			if errors.Is(ErrTooManyRequests, expErr) {
				t.Fatalf("Should not return too many request error as the last request should have executed after debounce duration: %v", ballotX)
			}
			t.Logf("Should not return too many request error as the last request should have executed after debounce duration: %v", checkMark)

			t.Logf("the service should only run once, the last operation in the cluster %v", checkMark)
		}
	}
}


func TestRetry(t *testing.T) {

	service := Retry(ForRetry(), 3, time.Second * 2)

	t.Log("Given the need to test that the service retries the request until success")
	{
		t.Log("When calling the `ForRetry Wrapper function` with default context value")
		{
			secret, err := service(context.Background())
			
			if err != nil {
				t.Fatalf("Should pass as retries exceeds service threshold: %v", ballotX)
			}

			if secret == "I AM THE ONE" {
				t.Logf("Should pass as retries exceeds service threshold: %v", checkMark)
			}
		}
	}
}

func TestThrottleLimitsRequests(t *testing.T) {
	results := []string{}
	var m sync.Mutex
	service := Throttle(ForThrottle(), 2, 2, time.Second*3)
	runs := 11
	ctx := context.Background()
	wg := sync.WaitGroup{}
	wg.Add(runs)

	t.Log("Given the need to test that the Throttle service limits requests to 2 every 3 seconds")
	{
		t.Logf("When calling the `ForThrottle Wrapper function` with default context value as %d goroutines", runs)
		{
			for range runs {
				go func() {
					defer wg.Done()
					response, err := service(ctx)
					if err == nil {
						m.Lock()
						results = append(results, response)
						m.Unlock()
					}
				}()
				time.Sleep(time.Second*1)
			}

			wg.Wait()

			expectedResults := 8
			if len(results) != expectedResults {
				t.Fatalf("Expected results length to be %d, but got %d: %v", expectedResults, len(results), ballotX)
			}
			t.Logf("Results length matches expected value of %d: %v", expectedResults, checkMark)
		
		}
	}
}






