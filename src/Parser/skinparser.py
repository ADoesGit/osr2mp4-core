# done by Kysan the gay pp farmer thanks

# return pos of the first char of the  comment or -1 if there is no comment
def detect_comments(line):
	ancient_char = ''
	for k in range(len(line)):
		if line[k] == '/' and ancient_char == '/':
			return k
		ancient_char = line[k]
	return -1


def del_comment(line):
	i = detect_comments(line)
	if i != -1:
		line = line[: i - 1]
	return line.strip()


settings = {}  # why not put all sections into it at the end ?


class Skin:
	def __init__(self, skin_path):
		# sections
		self.general = None
		self.colours = None
		self.fonts = None
		self.catchTheBeat = None
		self.mania = None
		self.skin_path = skin_path
		self.read()
		self.parse_general()
		self.parse_colors()
		self.parse_fonts()

		print(self.general)
		print(self.colours)
		print(self.fonts)

	def read(self):
		General = {}
		Colours = {}
		Fonts = {}
		CatchTheBeat = {}
		Mania = {}

		with open(self.skin_path + 'skin.ini', 'rb') as file:
			lines = file.readlines()

		for line in lines:
			# remove shit like `\r\n` and leading and trailling whitespaces
			line = line.decode().strip()

			# removing comments
			line = del_comment(line)

			# do not take care of void lines
			if line == '':
				continue

			# if section tag
			if line.startswith('[') and line.endswith(']'):

				if line in ['[General]',
				            '[Colours]',
				            '[Fonts]',
				            '[CatchTheBeat]',
				            '[Mania]']:
					section = line[1:-1]
					continue
				else:
					raise Exception('invalid section name found: ' + line[1:-1])

			sl = line.split(':')
			key, value = sl[0], sl[1]

			my_command = section + '["' + key + '"] = ' + '"' + str(value) + '"'
			exec(my_command)

		self.general = General
		self.colours = Colours
		self.fonts = Fonts
		self.catchTheBeat = CatchTheBeat
		self.mania = Mania

	def parse_general(self):
		self.general['CursorRotate'] = int(self.general.get('CursorRotate', 0))
		self.general['CursorExpand'] = int(self.general.get('CursorExpand', 0))
		self.general['CursorCentre'] = int(self.general.get('CursorCentre', 0))
		self.general['HitCircleOverlayAboveNumer'] = int(self.general.get('HitCircleOverlayAboveNumer', 0))
		self.general['SliderStyle'] = int(self.general.get('SliderStyle', 0))

	def parse_colors(self):
		for key, value in self.colours.items():
			value = value.split(",")
			for x in range(len(value)):
				value[x] = int(value[x])
			self.colours[key] = value

		cur_combo = 1
		while True:
			if "Combo" + str(cur_combo) in self.colours:
				cur_combo += 1
			else:
				break
		self.colours["Comb1"] = self.colours.get("Combo1", (255, 192, 0))
		self.colours["Comb2"] = self.colours.get("Combo2", (0, 202, 0))
		self.colours["Comb3"] = self.colours.get("Combo3", (18, 124, 255))
		self.colours["Comb3"] = self.colours.get("Combo4", (242, 24, 57))
		self.colours["InputOverlayText"] = self.colours.get("InputOverlayText", (0, 0, 0))
		self.colours["SliderBall"] = self.colours.get("SliderBall", (2, 170, 255))
		self.colours["SliderBorder"] = self.colours.get("SliderBorder", (255, 255, 255))
		self.colours["SliderTrackOverride"] = self.colours.get("SliderTrackOverride", (0, 0, 0))  # TODO: use current combo color
		self.colours["SpinnerBackground"] = self.colours.get("SpinnerBackground", (100, 100, 100))
		self.colours["ComboNumber"] = cur_combo - 1

	def parse_fonts(self):
		self.fonts['HitCircleOverlap'] = int(self.fonts.get('HitCircleOverlap', -2))
		self.fonts['ScoreOverlap'] = int(self.fonts.get('ScoreOverlap', -2))
		self.fonts['ComboOverlap'] = int(self.fonts.get('ScoreOverlap', -2))
		self.fonts['ComboPrefix'] = self.fonts.get('ComboPrefix', 'score')
		self.fonts['ComboPrefix'] = self.fonts['ComboPrefix'].replace(" ", "")
		self.fonts['ScorePrefix'] = self.fonts.get('ScorePrefix', 'score')
		self.fonts['ScorePrefix'] = self.fonts['ScorePrefix'].replace(" ", "")
		self.fonts['HitCirclePrefix'] = self.fonts.get('HitCirclePrefix', 'default')
		self.fonts['HitCirclePrefix'] = self.fonts['HitCirclePrefix'].replace(" ", "")


if __name__ == "__main__":
	skin = Skin("../../res/skin1/")