#
# Config Class for the requirements for rmtoo
#

class Config:
    # development - team at flonatel
    # users - users from the Internet (sourceforge replies and wishes)
    # customers - people and companies who are flonatel's customers
    stakeholders = ["development", "management", "users", "customers"]
    inventors = ["flonatel", ]

    reqs_dir = "doc/requirments"

    topic_specs = \
        {
          "ts_common": ["doc/topics", "ReqsDocument"],
        }

    output_specs = \
        [ 
          ["prios", 
           ["ts_common", "doc/latex2/reqsprios.tex"]],

          ["graph",
           ["ts_common", "req-graph1.dot"]],

          ["graph2",
           ["ts_common", "req-graph2.dot"]],

          ["stats_reqs_cnt", 
           ["ts_common", "doc/latex2/stats_reqs_cnt.csv"]],

          ["latex2", 
           ["ts_common", "doc/latex2/reqtopics.tex"]],

          ["html", 
           ["ts_common", 
            "doc/html/reqs", "doc/html/header.html",
            "doc/html/footer.html"]],
        ]
