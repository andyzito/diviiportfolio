(ns clojtest.core
  (:gen-class))

(def alphabet '(a b c d e f g h i j k l m n o p q r s t u v w x y z))
  
(defn -main
  []
  (println "Hello, World!"))

(defn letterfight
;; The original version of letterfight, which works, but is far less efficient
;; than the final version.
  [i lett1 lett2]
  (if (= lett1 (str (nth alphabet i)))
    true
    (if (= lett2 (str (nth alphabet i)))
      false
      (letterfight (inc i) lett1 lett2))))
  
(defn wordfight
;; the original version of wordfight, which is mostly the same as the final
;; version, except that it's handling of multiple arity arguments is a bit more
;; wordy.
  ([word1 word2]
  (def p 0)
  (if (= p (int (count (min-key count word1 word2))))
    (max-key count word1 word2)
    (do
      (def lett1 (subs word1 p (inc p)))
      (def lett2 (subs word2 p (inc p)))
      (if (= lett1 lett2)
        (wordfight word1 word2 (inc p))
        (if (= true (letterfight 0 lett1 lett2))
          word1
          word2)))))
  ([word1 word2 p]
    (if (= p (int (count (min-key count word1 word2))))
    (max-key count word1 word2)
    (do
      (def lett1 (subs word1 p (inc p)))
      (def lett2 (subs word2 p (inc p)))
      (if (= lett1 lett2)
        (wordfight word1 word2 (inc p))
        (if (= true (letterfight 0 lett1 lett2))
          word1
          word2))))))

(defn alphabetize
;; The original version of alphabetize, which does not work. It doesn't work
;; because I tried to alter the variable upon which the while loop condition
;; is based, which you can't do in Clojure I guess. The let statements which
;; tried to alter that variable only alter it inside themselves. So, yeah,
;; functional programming is weird and stuff.
  [one, two]
  (def raw one)
  (def ordered two)
  (while (> (count raw) 0)
  (do
    (let [ordered (concat ordered (reduce wordfight raw))])
    (let [raw (for [x raw
             :let [y x]
             :when (nil? (some #(= x %) ordered))]
             y)]))))


  
  
  