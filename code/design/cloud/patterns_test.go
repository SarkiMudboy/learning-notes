package main

import (
	"context"
	"errors"
	"testing"
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
	service := FaultyBreaker(ForCircuitBreaker(), 4)
	errChan := make(chan error, 3)
	ctx := context.Background()

	t.Log("Given the need to test that the Circuit stay closed when failure threshold has not been reached")
	{
		t.Log("When calling the `ForCircuitBreaker Wrapper function` as 4 goroutines with default context value")
		{
			for j := 0; j <= 3; j++ {

				go func() {
					e := service(ctx, "consecutive failures")
					errChan <- e
				}()
			}

			for j := 0; j <= 3; j++ {
				select {
					case err := <- errChan:
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

func TestBreakerTrips(t *testing.T) {
	service := FaultyBreaker(ForCircuitBreaker(), 4)
	errChan := make(chan error, 3)
	ctx := context.Background()
	var expErr error

	t.Log("Given the need to test that the Circuit opens when failure threshold has been reached")
	{
		t.Log("When calling the `ForCircuitBreaker Wrapper function` with default context value as 5 goroutines")
		{
			for j := 0; j <= 5; j++ {
				go func() {
					e := service(ctx, "consecutive failures")
					errChan <- e
				}()
			}

			for j := 0; j <= 5; j++ {
				select {
					case err := <- errChan:
						if errors.Is(ErrServiceUnavailable, err) {
							expErr = err
						}
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

// func TestFaultyBreaker(t *testing.T) {}
