# 🚀 Spacewalk-18 Benchmark 🛸

![teaser](assets/teaser.gif)

**Spacewalk-18: A Benchmark for Multimodal and Long-form Procedural Video Understanding** [[Paper](https://arxiv.org/abs/2311.18773)][[Project Page](https://brown-palm.github.io/Spacewalk-18/)]<br>
[Rohan Myer Krishnan*](https://scholar.google.com/citations?user=koxiPYIAAAAJ), [Zitian Tang*](https://zitiantang.github.io/), [Zhiqiu Yu](), [Chen Sun](https://chensun.me/index.html) (*Equal Contribution)

## Download Spacewalk-18

1. Clone this repository
```
git clone https://github.com/brown-palm/Spacewalk-18-benchmark.git
cd Spacewalk-18-benchmark
```

2. Download videos
```
cd data
python download_videos.py
```

## Dataset Structure

### Videos

The videos are downloaded into `data/videos`. There are in total 18 videos and each one is the recording of a spacewalk mission. All the videos are at `29.97 FPS` with frame size ``720 x 1280``.

### Transcripts
The transcripts of the videos are in [`data/transcripts`](data/transcripts). They contain the global start and end times of each sentence in seconds. Please use `encoding='cp1252'` when reading them.

### Steps and animations
At the beginning of each video, an animation demonstrates the mission to be done by the astronauts. Based off the animation, the mission is devided into dozens of steps, which are listed in [`data/steps.json`](data/steps.json).

| Field Name         | Description                                                         |
|--------------------|---------------------------------------------------------------------|
| index              | The index of the step in the corresponding spacewalk mission. Step 0 stands for ``Irrelevant'' label. |
| caption            | The caption of the step, which is a phrase or a short sentence.     |
| transcript         | The transcript of the animation clip of the step. It includes all the sentences intersecting with the time interval `[animation_start, animation_end]`.  |
| animation_start    | The global start time of the animation clip of the step in seconds. |
| animation_end      | The global end time of the animation clip of the step in seconds.   |

### Annotations

We annotate the spacewalk recordings by segmenting them into the steps. The annotations are in [`data/annotation.json`](data/annotation.json). Note that one step may occur multiple times and the steps may appear interwoven, because there are two astronauts working in parallel in a mission.

| Field Name         | Description                                                              |
|--------------------|--------------------------------------------------------------------------|
| video_start        | The global start time of the segment in seconds.                         |
| video_end          | The global end time of the segment in seconds.                           |
| frame_start        | The global start frame index of the segment.                             |
| frame_end          | The global end frame index of the segment.                               |
| label              | The step index that the segment belongs to. `-1` indicates unavailable.  |

## Tasks on Spacewalk-18
We have two tasks on Spacewalk-18 benchmark - [step recognition](#Task-1---Step-Recognition) and [intra-video retrieval](#Task-2---Intra-video-Retrieval). They share the same training, validation, and test video splits, which are listed in [`tasks/split.json`](tasks/split.json).

![task_img](assets/task_img.png)

### Task 1 - Step Recognition
Given a query timestamp $t$ in a video, step recognition aims to determine the step happening at $t$. The training, validation, and test samples are in `tasks/step_recognition/*.json`. We show in [`construct_samples.ipynb`](https://github.com/brown-palm/Spacewalk-18-benchmark/blob/main/tasks/step_recognition/construct_samples.ipynb) how they are constructed. You may use it to generate more training samples if they benefit your method. Moreover, we encourage you to go beyond these samples and fully use the training set videos to develop your model.

| Field Name         | Description                                            |
|--------------------|--------------------------------------------------------|
| timestamp          | The timestamp sampled as query timestamp $t$.        |
| frame_index        | The frame index of the query timestamp             |
| label              | The ground truth label of the sample.                  |
| id                 | A unique ID of the sample.                             |

Our tasks enables model evaluation under varying temporal context window lengths $w$. In this setting, a model needs to determine frame $t$'s corresponding step given the video clip $[t-w/2, t+w/2]$. We provide the code to calculate the video start and end times and collect the transcripts in the clip for any specified context length $w$. See [`construct_context_window.ipynb`](https://github.com/brown-palm/Spacewalk-18-benchmark/blob/main/tasks/step_recognition/construct_context_window.ipynb).

#### Evaluation Metrics
We use accuracy and mAP to evaluate the performance on the step recognition task. The code is in [`evaluation.py`](tasks/step_recognition/evaluation.py). To use it, please organize your predictions in a JSON file in the following format:
```
{
      "03152022": [
            {
                  "prediction": 1,
                  "score": [0.4, 0.8, ..., 0.2]
            },
            {
                  "prediction": 0,
                  "score": [0.9, 0.3, ..., 0.6]
            },
            ... ...
      ],
      "11152022": [
            ... ...
      ]
}
```
The $i$-th item under each video ID is your prediction to the $i$-th sample. `prediction` is a predicted label used to compute accuracy. `score` is a list of scores for each category used to compute mAP. The length of `score` should be the same as the number of categories in the corresponding video. If your method does not provide category scores, you can omit `score` in your file.

You can use `--gt` to specify the ground truth file and `--pred` to specify your prediction file. For example, to evaluate your predictions on the validation set, run
```
python evaluation.py \
--gt val.json \
--pred YOUR_PREDICTION_FILE.json
```

### Task 2 - Intra-video Retrieval
Given a query timestamp $t_q$ and two candidate timestamps $t_1$ and $t_2$, intra-video retrieval aims to determine which candidate comes from the same step as the query. The training, validation, and test samples are in `tasks/intra-video_retrieval/*.json`. We show in [`construct_samples.ipynb`](https://github.com/brown-palm/Spacewalk-18-benchmark/blob/main/tasks/intra-video_retrieval/construct_samples.ipynb) how they are constructed. Again, we encourage you to go beyond the provided training samples to develop your model.

| Field Name               | Description                                          |
|--------------------------|------------------------------------------------------|
| query_frame_index        | The frame index of the query timestamp $t_q$.        |
| candidate_frame_indices  | A list of length 2. The frame indices of the candidate timestamps $t_1$ and $t_2$.        |
| label                    | The ground truth label with value `0` or `1` indicating which candidate belongs to the same step as the query.       |
| id                       | A unique ID of the sample.                           |

With a temporal context window length $w$, the model can access to video clips $[t_q-w/2, t_q+w/2]$, $[t_1-w/2, t_1+w/2]$, and $[t_2-w/2, t_2+w/2]$. We provide the code to calculate the video start and end times and collect the transcripts for any specified context length $w$. See [`construct_context_window.ipynb`](https://github.com/brown-palm/Spacewalk-18-benchmark/blob/main/tasks/intra-video_retrieval/construct_context_window.ipynb).

#### Evaluation Metrics
We use accuracy evaluate the performance on the intra-video retrieval task. The code is in [`evaluation.py`](tasks/intra-video_retrieval/evaluation.py). Please organize your predictions in a JSON file in the following format:
```
{
      "03152022": [1, 0, 1, 1, ..., 1],
      "11152022": [1, 0, 0, 1, ..., 0],
      ... ...
}
```
The list under each video ID is your predictions to the samples. Their values should be either `0` or `1`.

You can use `--gt` to specify the ground truth file and `--pred` to specify your prediction file. For example, to evaluate your predictions on the validation set, run
```
python evaluation.py \
--gt val.json \
--pred YOUR_PREDICTION_FILE.json
```

## Citation

We will be happy if you find Spacewalk-18 useful. Please cite it using this BibTeX:
```
@misc{krishnan2024spacewalk18,
      title={Spacewalk-18: A Benchmark for Multimodal and Long-form Procedural Video Understanding}, 
      author={Rohan Myer Krishnan and Zitian Tang and Zhiqiu Yu and Chen Sun},
      year={2024},
      publisher={arXiv:2311.18773}
}
```

## LICENSE
Spacewalk-18 benchmark is released under [MIT License](LICENSE).