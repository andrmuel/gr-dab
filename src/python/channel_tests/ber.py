def bits_set(x):
	bits = 0
	for i in range(0,8):
		if (x & (1<<i))>0:
			bits += 1
	return bits

def find_ber(sent, received):
	assert(len(received)<=len(sent))
	if len(received) < len(sent)/2:
		print "frame detection error, more than half of the frames were lost!"
		return 0.5
	errors = 0
	for i in range(0,len(received)):
		errors += bits_set(sent[i] ^ received[i]) # ^ is xor
	return float(errors)/float(8*len(received))

