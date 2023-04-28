import csv
from processor.frame import Frame

def frames_to_csv(filename: str, frames: "list[Frame]"):
    with open(filename, 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['qid', 'image', 'percent', 'comment', 'shorts', 'video', 'video_action', 'news'])
        # writer.writerow(['user', 'qid', 'image', 'picture_number', 'pid', 'percent', 'biggest', 'context', 'code_id', 'comment', 'shorts', 'video', 'video_action', 'news'])
        
        for frame in frames:
            for pid in range(len(frame.contexts)):
                writer.writerow([
                    frame.basic_info.user,
                    frame.basic_info.qid,
                    frame.basic_info.path,
                    frame.basic_info.picture_number,
                    pid,
                    frame.percentages[pid],
                    int(frame.biggests[pid]),
                    frame.contexts[pid],
                    frame.code_ids[pid],
                    int(frame.is_comment),
                    int(frame.is_shorts),
                    int(frame.is_video),
                    int(frame.is_action),
                    int(frame.is_news),
                ])

def frames_to_evaluation_csv(filename: str, frames: "list[Frame]"):
    with open(filename, 'w', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['qid', 'image', 'width', 'height', 'comment', 'video', 'video_action', 'shorts', 'border'])
        
        for frame in frames:
            writer.writerow([
                frame.basic_info.qid,
                frame.basic_info.path,
                frame.basic_info.frame_size[1],
                frame.basic_info.frame_size[0],
                int(frame.is_comment),
                int(frame.is_video),
                int(frame.is_action),
                int(frame.is_shorts),
                frame.borders,
            ])