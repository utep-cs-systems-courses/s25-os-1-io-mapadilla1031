#@author Marko Padilla 
#CS 4375
#Lab01 - io Introduction
#Last date modified 02/09/25
import os
import re
import sys

def read_file(fd):
    data = b""

    while True:
        read_bytes = os.read(fd, 1000)#read part, for 1000 bytes
        if not read_bytes:
            break
        data += read_bytes

    return data.decode('ascii')

def fix_count_words(text):
    text = re.sub(r"[^a-z\s]", "", text.lower())  #only lowercase and spaces allowed

    words = text.split()

    word_counts = {}  # Dictionary to store word frequencies
    for word in words:
        if word in word_counts:  # Check if word is in dictionary
            word_counts[word] += 1  # +1 count
        else:
            word_counts[word] = 1  # Init count

    word_counts_array = []
    for word in word_counts:
        word_counts_array += [(word, word_counts[word])]

    selection_sort(word_counts_array)
    return word_counts_array

def selection_sort(word_counts_array):#sort alpha order
    n = 0
    for item in word_counts_array:
        n += 1

    for i in range(n):
        min_index = i  
        for j in range(i + 1, n):
            if word_counts_array[j][0] < word_counts_array[min_index][0]:
                min_index = j
        word_counts_array[i], word_counts_array[min_index] = word_counts_array[min_index], word_counts_array[i]

def write_to_file(fd_out, sorted_words):
    for word, count in sorted_words:
        buffer = f"{word} {count}\n".encode()#convert to bytes
        while buffer:
            wc = os.write(fd_out, buffer)#write from buffer to output file
            buffer = buffer[wc:]# Slice off the first wc bytes, write remaining.

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    fd_input = os.open(input_file, os.O_RDONLY)
    fd_output = os.open(output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)

    text = read_file(fd_input)
    sorted_words = fix_count_words(text)
    write_to_file(fd_output, sorted_words)

    os.close(fd_input)
    os.close(fd_output)

if __name__ == "__main__":
    main()
