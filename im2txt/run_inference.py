# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""Generate captions for images using default beam search parameters."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
import datetime


import tensorflow as tf

from im2txt import configuration
from im2txt import inference_wrapper
from im2txt.inference_utils import caption_generator
from im2txt.inference_utils import vocabulary

class TimerMgr:
  def __init__(self):
    self.start_time = None
    self.end_time = None
  
  def start(self):
    self.start_time = datetime.datetime.now()
  
  def end(self):
    self.end_time = datetime.datetime.now()
  
  def __str__(self):
    diff = self.end_time - self.start_time
    return "took " + str(diff.total_seconds()) + " seconds."

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string("checkpoint_path", "",
                       "Model checkpoint file or directory containing a "
                       "model checkpoint file.")
tf.flags.DEFINE_string("vocab_file", "", "Text file containing the vocabulary.")
tf.flags.DEFINE_string("input_files", "",
                       "File pattern or comma-separated list of file patterns "
                       "of image files.")
tf.flags.DEFINE_string("output_caption_file","", "file name where captions generated will be saved")

tf.logging.set_verbosity(tf.logging.INFO)


def main(_):
  t = TimerMgr()
  

  # Build the inference graph.
  g = tf.Graph()
  with g.as_default():
    model = inference_wrapper.InferenceWrapper()
    restore_fn = model.build_graph_from_config(configuration.ModelConfig(),
                                               FLAGS.checkpoint_path)
  g.finalize()

  # Create the vocabulary.
  vocab = vocabulary.Vocabulary(FLAGS.vocab_file)

  filenames = []
  for file_pattern in FLAGS.input_files.split(","):
    filenames.extend(tf.gfile.Glob(file_pattern))
  tf.logging.info("Running caption generation on %d files matching %s",
                  len(filenames), FLAGS.input_files)

  
  with tf.Session(graph=g) as sess:
    # Load the model from checkpoint.
    restore_fn(sess)

    # Prepare the caption generator. Here we are implicitly using the default
    # beam search parameters. See caption_generator.py for a description of the
    # available beam search parameters.
    generator = caption_generator.CaptionGenerator(model, vocab, beam_size=100, max_caption_length=25)

    # save captions file
    fop = open(FLAGS.output_caption_file, "w", encoding="utf-8")

    t.start()
    cnt = 0
    for filename in filenames:
      with tf.gfile.GFile(filename, "rb") as f:
        image = f.read()
      captions = generator.beam_search(sess, image)
      # print("Captions for image %s:" % os.path.basename(filename))
      buff = filename + "\t"
      for i, caption in enumerate(captions):
        # Ignore begin and end words.
        sentence = [vocab.id_to_word(w) for w in caption.sentence[1:-1]]
        sentence = " ".join(sentence)
        # print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))

        buff += sentence +"["+ str(math.exp(caption.logprob)) + "]|"
        cnt += 1

        if cnt % 100 is 1:
          print("Captioned " + str(cnt) + " files.")

      fop.write(buff+"\n")
    print("Completed captioning " + str(cnt) + " files.")
    fop.close()

    t.end()
    print(t)


if __name__ == "__main__":
  tf.app.run()