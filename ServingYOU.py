import falcon
import os, time
#import json 
#from models.user import User

class GetSongsResource:
	_MP3s_File = 'adam_mp3s.html'
	_MP3s_Modify_Date = None
	_MP3s_last_modified = ''
	_Num_Visits = 0
	mp3s_list = ''

	def mp3s_modify_date_updated(self):
		wasUpdated = False
		moddate  = os.stat(self._MP3s_File)[8]	# Thanks to: https://mygisblog.wordpress.com/2014/08/03/monitoring-if-a-file-has-changed-in-python/
		if  self._MP3s_Modify_Date != moddate:
			self._MP3s_Modify_Date = moddate	# Keep the latest modification date
			self._MP3s_last_modified = time.ctime(moddate)
			wasUpdated = True
			print("\n mp3s_modify_date_updated() : " + str(wasUpdated) )
			print("\n moddate = {}\n _MP3s_Modify_Date = {}\n _MP3s_last_modified  = {}".format(moddate, self._MP3s_Modify_Date, self._MP3s_last_modified) )
		else:
			wasUpdated = False

		return wasUpdated

	def visitors_count(self):
		self._Num_Visits += 1
		return """Page Visited <span style="color:#9ac400; font-weight:bold"> %s </span> times <br /><br />""" % ( str(self._Num_Visits) )

	def on_get(self, req, resp):
		"""Handles GET requests"""

		if not os.path.isfile( self._MP3s_File ):
			self.mp3s_list = "The file '{}' is missing!".format(self._MP3s_File)
			resp.status = falcon.HTTP_500
		elif self.mp3s_modify_date_updated():
			self.mp3s_list = """<u>Last Modified</u>: %s <br /><br />""" % self._MP3s_last_modified
			# The file must exist if we reached here... so read its content
			file = open( self._MP3s_File, 'r', encoding='utf8', errors='ignore')	# Thanks to: https://github.com/minimaxir/textgenrnn/issues/8
			self.mp3s_list += file.read().rstrip()
			file.close()
			resp.status = falcon.HTTP_200

		# Make sure page is set to UTF-8 because this default changes when content_type = 'text/html' ( https://github.com/falconry/falcon/issues/145 )
		self.mp3s_list_Head = """<head> <meta charset="UTF-8">
								 <title> Serving you Adam's MP3s Playlist every day, hour and minute... of the Week! :) </title>
								 </head>"""		
		resp.content_type = 'text/html'	  # we want a regular webpage ...  not json
		resp.body = self.mp3s_list_Head + self.visitors_count() + self.mp3s_list

api = falcon.API()
api.add_route('/songs', GetSongsResource())
