Description
-----------

This pipeline maps your reads to a given reference, marks duplicate
reads (if not instructed otherwise), realigns your reads with ``lofreq
viterbi``, recalibrates base qualities with Lacer (author:
`Swaine Chen <mailto:slchen@gis.a-star.edu.sg>`_) and calls SNVs and indels with `LoFreq
<http://csb5.github.io/lofreq/>`_.


How to
------

- Run ``variant-calling-lofreq.py -h`` to get basic usage information.
- If called correctly, jobs will be run on the cluster automatically
- Using ``-v`` is recommended to get some more information
- Should the pipeline 'crash', it can be restarted by simply running
  ``bash run.sh`` (for local mode) or ``qsub run.sh`` (for cluster
  mode).  Note that a crash due to input file or parameter issues can
  not be resolved in this fashion.


Output
------

- The main log file is ``./logs/snakemake.log``
- After a successful run the last line in the snakemake log file will say ``(100%) done``
- All output files can be found in ``./out/``
- Furthermore a simple report have been generated (``./out/report.html``)
- Parameters including program versions etc. can be found in ``conf.yaml``




