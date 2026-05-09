package main

import "sync"


type Future interface {
	Result() (string, error)
}


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

func Split(source <-chan int, num int) []chan int {
	out := make([]chan int, num)
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


type InnerFuture struct {
	// sync
	once sync.Once
	wg sync.WaitGroup

	// values
	res string
	err error

	// channels
	resCh chan string
	errCh chan error
}


func NewInnerFuture(r chan string, e chan error) *InnerFuture {
	return &InnerFuture{
		resCh: r,
		errCh: e,
	}
}


func (i *InnerFuture) Result() (string, error) {
	i.once.Do(func() {
		i.wg.Add(1)
		defer i.wg.Done()
		i.res = <- i.resCh
		i.err = <- i.errCh
	})
  // wait
	i.wg.Wait()
	return i.res, i.err
}
