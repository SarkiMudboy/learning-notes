package main

import (
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
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			result, err := ForFanOut(tc.batchSize, tc.value)
			if result != tc.expectedResult {
				t.Errorf("expected value %d, got %d", tc.expectedResult, result)	
			}
				t.Logf("Result match %d : %d", tc.expectedResult, result)

				if errors.Is(tc.expectedErr, err) {
					t.Errorf("Errors do not match") 
				}
				t.Logf("Errors match bro")
		})
	}
}
