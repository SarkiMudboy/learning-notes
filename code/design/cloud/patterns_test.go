package main

import (
	"context"
	"errors"
	"fmt"
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

func TestCircuitBreakerFails(t *testing.T) {

	service := Breaker(ForCircuitBreaker(), 4)

	testCases := [] struct {
		Name string
		Case string
		When string
		Success string
		Fail string
		Runs int
		Workflow string
		ExpErr error
	}{
		{
			Name: "TestCircuitBreakerStayClosed",
			Case: "Given the need to test that the Circuit stay closed when failure threshold has not been reached",
			When: "When calling the `ForCircuitBreaker Wrapper function` with default context value 3 times",
			Success: fmt.Sprintf("Should return only Service Failure errors as Breaker threshold limit has not being hit: %v", checkMark),
			Fail: fmt.Sprintf("Should return only Service Failure errors as Breaker threshold limit has not being hit: %v", ballotX),
			Runs: 3,
			Workflow: "consecutive failures",
			ExpErr: ErrServiceFailure,
		},
		{
			Name: "TestCircuitBreakerOpens",
			Case: "Given the need to test that the Circuit opens when failure threshold has been reached",
			When: "When calling the `ForCircuitBreaker Wrapper function` with default context value 5 times",
			Success: fmt.Sprintf("Should return Service Unavailable errors as Breaker threshold limit has being hit: %v", checkMark),
			Fail: fmt.Sprintf("Should return Service Unavailable errors as Breaker threshold limit has being hit: %v", ballotX),
			Runs: 3,
			Workflow: "consecutive failures",
			ExpErr: ErrServiceUnavailable,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.Name, func(t *testing.T) {
			t.Log(tc.Case)
			{
				t.Log(tc.When)
				{
					for j := 0; j <= tc.Runs; j++ {
						err := service(context.Background(), tc.Workflow)
						if !errors.Is(tc.ExpErr, err) {
							t.Fatal(tc.Fail)
						}
					}
					t.Logf(tc.Success)
				}
			}
		})
	}
	
}