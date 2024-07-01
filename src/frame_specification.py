from database_interaction import connect_to_db, get_visual_representation

def create_frame_specifications(ner_results):
    session = connect_to_db()
    frames = []
    for entity in ner_results:
        visual_link = get_visual_representation(entity['word'], session)
        frame = {
            'entity': entity['word'],
            'type': entity['entity'],
            'visual_link': visual_link
        }
        frames.append(frame)
    return frames
