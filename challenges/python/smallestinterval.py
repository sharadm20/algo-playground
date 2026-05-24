import heapq
from numpy import inf


def smallest_interval(nums):
	# initialize heap. each tuple contains (value, which list it is from, index within that list)
	heap = [(row[0], i, 0) for i, row in enumerate(nums)]

	heapq.heapify(heap)
    
	# initialize local_maximum and answer
	local_maximum = max(row[0] for row in nums)
	ans = [-inf, inf]
	while heap:
		# pop local_minimum from the heap		local_minimum, num_list, local_min_index = heapq.heappop(heap)

		# if the new interval is smaller than tracked interval, update tracked interval
		if local_maximum - local_minimum < ans[1] - ans[0]:
			ans = [local_minimum, local_maximum]

		# if we've reached the end of this list, we know we've seen all possible intervals.
		if local_min_index + 1 == len(nums[num_list]):
			return ans

		# increment the local_min_index and recalculate local_maximum
		next_val = (nums[num_list][local_min_index +1])
		local_maximum = max(next_val, local_maximum)

		# push the new element onto the heap
		heapq.heappush(heap, (next_val, num_list, local_min_index+1))

num = [[0, 1, 4, 17, 20, 25, 31],
 [5, 6, 10],
 [0, 3, 7, 8, 12]]
result = smallest_interval(num)
print(result)