(ns clojtest.core
  (:gen-class))

(def alphabet 
  (map str '(a b c d e f g h i j k l m n o p q r s t u v w x y z)))
  
(defn -main
  []
  (println "Hello, World!"))

(defn letterfight
;; ALL credit to Lee, copypasted from his email.
;; This function returns true if lett1 is earlier in the alphabet,
;; and false if lett2 is.
  [lett1 lett2]
  (< (count (take-while #(not (= lett1 %)) alphabet))
     (count (take-while #(not (= lett2 %)) alphabet))))
  
(defn wordfight
;; Returns the word with higher alphabetical priority.
  ([word1 word2] (wordfight word1 word2 0)) ;; If no positional argument is given, sets position to 0
  ([word1 word2 p]
;; This if statement handles the case of two words which are identical except
;; for a suffix, for example "cat" and "cats".
    (if (= p (int (count (min-key count word1 word2))))
    (min-key count word1 word2)
    (do
      (def lett1 (subs word1 p (inc p)))
      (def lett2 (subs word2 p (inc p)))
      (if (= lett1 lett2)
        (wordfight word1 word2 (inc p))
        (if (= true (letterfight lett1 lett2))
          word1
          word2))))))

(defn alphabetize
;; Returns an alphabetically sorted vector, given an unsorted vector.
;; ALL credit to Lee for this function, copy-pasted from his email.
  [words]
  (loop [unsorted words
         sorted []]
    (if (empty? unsorted)
      sorted
      (let [first-word (reduce wordfight unsorted)]
        (recur (remove #(= first-word %) unsorted)
               (conj sorted first-word))))))