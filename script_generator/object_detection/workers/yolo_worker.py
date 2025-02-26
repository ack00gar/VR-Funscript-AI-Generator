import time

from script_generator.constants import YOLO_CONF, YOLO_BATCH_SIZE, YOLO_PERSIST
from script_generator.debug.logger import log_od
from script_generator.tasks.workers.abstract_task_processor import AbstractTaskProcessor, TaskProcessorTypes


class YoloWorker(AbstractTaskProcessor):
    process_type = TaskProcessorTypes.YOLO

    # TODO add pose model support
    # if run_pose_model:
    #     yolo_pose_results = pose_model.track(frame, persist=True, conf=YOLO_CONF, verbose=False)

    def task_logic(self):
        batch = []
        tasks = []

        for task in self.get_task():
            if task.rendered_frame is not None:
                batch.append(task.rendered_frame)
                tasks.append(task)

                # If batch is ready, process it
                if len(batch) >= YOLO_BATCH_SIZE:
                    self.process_batch(batch, tasks)
                    batch = []
                    tasks = []
            else:
                log_od.warn(f"Rendered frame missing on Yolo task")

        # Process any remaining tasks in the batch with padding
        if batch:
            # Pad the batch with the last frame to reach YOLO_BATCH_SIZE
            last_frame = batch[-1]
            while len(batch) < YOLO_BATCH_SIZE:
                batch.append(last_frame.copy())

            self.process_batch(batch, tasks)

    def process_batch(self, frames, tasks):
        start_time = time.time()
        # Yolo expects bgr images when using numpy frames
        # yolo_results = self.state.yolo_model(frames, conf=YOLO_CONF, verbose=False) # replace with this line for pipeline speed testing
        yolo_results = self.state.yolo_model.track(frames, persist=YOLO_PERSIST, conf=YOLO_CONF, verbose=False) # , tracker="bytetrack.yaml") # , iou=0.5, show=True
        avg_time = (time.time() - start_time) / len(tasks)  # Use original tasks length, not padded

        # Only process the actual tasks, ignore padded results
        for t, result in zip(tasks, yolo_results[:len(tasks)]):
            t.yolo_results = result
            t.duration(str(self.process_type), avg_time)
            self.finish_task(t)
