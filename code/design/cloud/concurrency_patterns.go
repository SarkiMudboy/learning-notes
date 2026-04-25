package main

import "sync"

func Funnel(sources ...<-chan int) <-chan int {
	out := make(chan int)

	wg := sync.WaitGroup{}
	for _, source := range sources {
		wg.Add(1)
		go func(source <-chan int) {
			for s := range source {
				out <- s
			}
			wg.Done()
		}(source)
	}
	go func() {
		wg.Wait()
		close(out)
	}()
	return out
}

func Split(source <-chan int, num int) []chan<- int {
	out := make([]chan<- int, num)
	for i := 0; i < num; i++ {
		ch := make(chan int)
		out[i] = ch

		go func() {
			defer close(ch)
			for val := range source {
				out[i] <- val
			}
		}()
	}
	return out
}
