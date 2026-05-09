package main

import (
	"context"
	"errors"
	"testing"
)

func TestFanIn(t *testing.T) {
	testCases := []struct {
		name         string
		numOfSources int
		numOfValues  int
		expectedLen  int
	}{
		{
			name:         "3 sources, 5 values",
			numOfSources: 3,
			numOfValues:  5,
			expectedLen:  15,
		},
		{
			name:         "4 sources, 3 values",
			numOfSources: 4,
			numOfValues:  3,
			expectedLen:  12,
		},
		{
			name:         "",
			numOfSources: 4,
			numOfValues:  0,
			expectedLen:  0,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			result := ForFanIn(tc.numOfSources, tc.numOfValues)
			if len(result) != tc.expectedLen {
				t.Errorf("expected length %d, got %d", tc.expectedLen, len(result))
			}
			t.Logf("Length match %d : %d", tc.expectedLen, len(result))
		})
	}
}


func TestFanOut(t *testing.T) {
	testCases := []struct{
		name string
		batchSize int
		value int
		expectedResult int
		expectedErr error
	} {
		{
			name: "value of 10 and size of 5",
			batchSize: 5,
			value: 10,
			expectedResult: 3628800,
			expectedErr: nil,
		},
		{
			name: "value of 20 and size of 8",
			batchSize: 8,
			value: 20,
			expectedResult: 0,
			expectedErr: ErrInvalidInput,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// result, err := ForFanOut(tc.batchSize, tc.value)
			result, err := ForFanOutRoundRobin(tc.batchSize, tc.value)
			if result != tc.expectedResult {
				t.Errorf("expected value %d, got %d - %v", tc.expectedResult, result, ballotX)	
			} else {
				t.Logf("Result match %d : %d - %v", tc.expectedResult, result, checkMark)
			}
			if !errors.Is(tc.expectedErr, err) {
				t.Errorf("Errors do not match, expected %v got %v - %v", tc.expectedErr, err, ballotX) 
			} else {
				t.Logf("Errors match, %v", checkMark)
			}
		})
	}
}


func TestFuture(t *testing.T) {
	// pass a duration to for future
	// immediately read from the future: test that it does not error rather blocks 
	// test that the return values are correct and
	// test that subsequest reads do not delay (return cached values)
	ctx := context.Background()
	
	t.Log("Given the need to test that the Future does not throw an error for early read")

	{	
		t.Log("When calling the `ForFuture` with default context value and a delay of 10 secs")
		{
			future := ForFuture(ctx, 10, ServiceResponse)
			res, err := future.Result()
			if err != nil {
				t.Errorf("Failed with error: %v %v\n", err, ballotX)
			}
			
			if res != ServiceResponse {
				t.Errorf("Results do not match, Expected %s got %s %v\n", ServiceResponse, res, ballotX)	
			}
			t.Logf("Results match %v", checkMark)
		}
	}


}



