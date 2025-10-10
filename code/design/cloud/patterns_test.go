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
	service := Breaker(ForCircuitBreaker(), 4)

	t.Log("Given the need to test that the Circuit stay closed when failure threshold has not been reached")
	{
		t.Log("When calling the `ForCircuitBreaker Wrapper function` with default context value 3 times")
		{
			for j := 0; j <= 3; j++ {
				err := service(context.Background(), "consecutive failures")
				if !errors.Is(ErrServiceFailure, err) {
					t.Fatalf("Should return only Service Failure errors as Breaker threshold limit has not being hit: %v", ballotX)
				}
			}
			t.Logf("Should return only Service Failure errors as Breaker threshold limit has not being hit: %v", checkMark)
		}
	}
	
}

func TestBreakerOpens(t *testing.T) {
	service := Breaker(ForCircuitBreaker(), 4)
	var expErr error

	t.Log("Given the need to test that the Circuit opens when failure threshold has been reached")
	{
		t.Log("When calling the `ForCircuitBreaker Wrapper function` with default context value 5 times")
		{
			for j := 0; j <= 5; j++ {
				expErr = service(context.Background(), "consecutive failures")
			}
			if !errors.Is(ErrServiceUnavailable, expErr) {
				t.Fatalf("Should return Service Unavailable errors as Breaker threshold limit has being hit: %v", ballotX)
			}
			t.Logf("Should return Service Unavailable errors as Breaker threshold limit has being hit: %v", checkMark)
		}
	}
	
}
