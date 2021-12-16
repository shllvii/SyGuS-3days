(set-logic LIA)


(synth-fun rec ((x Int) (y Int)) Int
  (
    (Start Int (x
                y
                (+ Start Start)
                (- Start Start)
    ))))

(declare-var x Int)
(declare-var y Int)

(constraint (= (rec x y) (+ x y)))

(check-synth)