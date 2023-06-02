
#import required libraries
from pydub import AudioSegment
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS


SPLIT_PARTS_S = 60 * 10
SPLIT_PARTS_MS = SPLIT_PARTS_S * 1000

num_eps = 1
class Silence:
    def __init__(self, start, end, delay):
        self.start = round(start + delay, 2)
        self.end = round(end + delay, 2)
        self.duration = end - start
    
    def __lt__(self, other):
        return self.duration < other.duration

    def __repr__(self) -> str:
        return f"<S duration={self.duration}, start={self.start} end={self.end} />"


def split_audio(path) -> list:
    parts = []

    eps = AudioSegment.from_mp3(path)
    for i, part in enumerate(eps[::SPLIT_PARTS_MS]):
        part_path = f'./processing/part-{i}.mp3'
        part.export(part_path, format="mp3")
        parts.append(part_path)

    return parts


def silences_of_part(part_path, part_num, plot=False):
    # below method returns the active / non silent segments of the audio file 
    [Fs, x] = aIO.read_audio_file(part_path)
    segments = aS.silence_removal(x, 
                                Fs, 
                                0.020, 
                                0.020, 
                                smooth_window=1.0, 
                                weight=0.3, 
                                plot=plot)

    curr_sec = 0
    silences = []
    for seg in segments:
        s = Silence(curr_sec, seg[0], SPLIT_PARTS_S * part_num)
        if s.duration > 3:
            silences.append(s)
        curr_sec = seg[1]

    silences.sort(reverse=True)
    return silences


def merge_silences(silences_by_parts: dict[int, list[Silence]]) -> list:
    silences = []

    for part_num in range(len(silences_by_parts) - 1):
        part_silences = silences_by_parts[part_num]
        next_part_silences = silences_by_parts[part_num + 1]
        
        if (len(part_silences) > 0) and (len(next_part_silences) > 0):
            part_last_silence = part_silences[-1]
            next_part_first_silence = part_silences[0]
            
            if (next_part_first_silence.duration - part_last_silence.duration < 0.2):
                silences.extend(part_silences[:-1])
                merged_silence = Silence(part_last_silence.start, next_part_first_silence.end)
                silences.extend(merged_silence)

        silences.extend(part_silences)
    




def main():
    # path to audio file
    path="./data/eps-1.mp3"
    silences_of_part(path, 0, False)
    # parts_paths = split_audio(path)

    # silences_by_parts = {}

    # for i, part_path in enumerate(parts_paths):
    #     silences_by_parts[i] = silences_of_part(part_path, i)
    


    # # below method returns the active / non silent segments of the audio file 
    # [Fs, x] = aIO.read_audio_file(path)
    # segments = aS.silence_removal(x, 
    #                             Fs, 
    #                             0.020, 
    #                             0.020, 
    #                             smooth_window=1.0, 
    #                             weight=0.3, 
    #                             plot=False)

    # curr_sec = 0
    # silences = []
    # for seg in segments:
    #     silences.append(Silence(curr_sec, seg[0]))
    #     curr_sec = seg[1]

    # silences.sort(reverse=True)
    # print(silences)

if __name__ == '__main__':
    main()