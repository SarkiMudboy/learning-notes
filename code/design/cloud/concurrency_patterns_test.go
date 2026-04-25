package main

import "testing"

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
