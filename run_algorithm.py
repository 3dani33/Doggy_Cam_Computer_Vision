"""This module is the commandline interface to the algorithm.

It handles the commandline interface, the files and the extraction of images from
the videos. If a reference file is found, the reference is also shown in the video.

Run the motion detection algorithm on the given file.
It can show the processing happening live. The current motion detection
output is shown as a colored circle on top of the video in green (calm) or 
red (motion detected).
The output is saved in the folder output.
The execution can be quit by pressing q, when focusing the output window."""

import plac
import numpy as np
import cv2
import os
from algorithm import motion_detection, get_algorithm_version
import file_handler
from evaluate_algorithm import update_frame_count


RED = (0, 0, 255)
WHITE = (255, 255, 255)

def load_video(file):
	video = cv2.VideoCapture(file)
	framerate = video.get(cv2.CAP_PROP_FPS)
	frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	print('framerate: {}, frame count: {}'.format(framerate, frame_count))
	return (video, framerate, frame_count)

@plac.pos('file', 'The video file path to run the algorithm on.')
@plac.flg('show', 'Show the algorithm output live')
def run_algorithm(file: str, show: bool=False) -> None:

	filename = os.path.basename(file)
	print('Run algorithm on file: {}'.format(filename))
	
	# load video
	video, framerate, frame_count = load_video(file)

	# try to find reference file
	reference_available, reference = file_handler.load_reference_data(filename)
	reference = update_frame_count(frame_count, reference)

	# processing loop
	result = np.zeros(frame_count ,dtype=bool)
	intensity = np.zeros(frame_count)
	for n in range(frame_count):
		_, frame = video.read()

		# error in frame count
		if frame is None:
			print('End of video! frame {} of {}'.format(n, frame_count))
			print('Slicing result list to match new frame count: {}'.format(n))
			result = result[:n]
			frame_count = n
			break

		# pass image to run_algorithm and save the result
		result[n], intensity[n], img_back_sub = motion_detection(frame)

		if show:
			# add indicator for reference
			if reference_available:

				col = RED if reference['reference'][n] else WHITE
				cv2.circle(frame, center=(10, 10), radius=10, color=col, thickness=-1)
				cv2.circle(img_back_sub, center=(10, 10), radius=10, color=col, thickness=-1)
				# grab a few frames with motion
				# if col == RED and n < 50:
				# 	cv2.imwrite('img/filter_noise_{}.png'.format(n), img_back_sub)

			# add indicator for algorithm
			col = RED if result[n] else WHITE
			cv2.circle(frame, center=(20, 10), radius=10, color=col, thickness=-1)
			cv2.circle(img_back_sub, center=(20, 10), radius=10, color=col, thickness=-1)

			# add frame number
			font = cv2.FONT_HERSHEY_SIMPLEX
			string = '{}/{}'.format(n,frame_count)
			cv2.putText(frame, string, (100,15), font, 0.5,(255,255,255), 1, cv2.LINE_AA)
			cv2.putText(img_back_sub, string, (100,15), font, 0.5,(255,255,255), 1, cv2.LINE_AA)
			

			# show image
			cv2.imshow('Doggy Cam: Standard View', frame)
			cv2.imshow('Doggy Cam: Background Substraction', img_back_sub)

		key = cv2.waitKey(1)
		if key & 0xFF == ord('q'):
			# allow quitting by pressing q
			print('Quitting...')
			exit()

	

	# 2-D array with intensity and the annotated values for 
	# clean up, if wrong frame_count can be fixed
	temp = np.vstack((reference['reference'],intensity))
	temp = temp.T

	# export temp to csv 
	file_handler.save_csv(filename, get_algorithm_version(), temp)

	# save result with framerate and frame count in pickle file
	file_handler.save_algorithm_result(filename, framerate, frame_count, result, get_algorithm_version())

if __name__ == '__main__':
	plac.call(run_algorithm)