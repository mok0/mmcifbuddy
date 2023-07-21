SHELL=/bin/sh

all: test_strtok_r 

test_strtok_r: test_strtok_r.o
	$(CC) $^ -o $@

.PHONY: clean
clean:
	$(RM)  *.o *~
