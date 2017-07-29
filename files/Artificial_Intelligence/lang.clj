(ns words2.core
  (:gen-class))

(require '[clojure.string :as s])

;; Like (contains?) but for vectors instead of maps, 
;; copied from a comment on http://stackoverflow.com/questions/3249334/test-whether-a-list-contains-a-specific-value-in-clojure
(defn in?
  [seq elm]  
  (if (not= nil (some #(= elm %) seq))
    true
    false))

;; combining single words into phrase chunks
(def phrase-rules
  {['article 'noun] 'art-phrase
   ['article 'noun-phrase] 'art-phrase
   ['adjective 'noun] 'noun-phrase
   ['adjective 'noun-phrase] 'noun-phrase
   ['verb 'noun-phrase] 'verb-phrase
   ['preposition 'noun-phrase] 'prep-phrase
   ['preposition 'art-phrase] 'prep-phrase})

;; what order can things go in?
(def rules
  [
   ['noun-phrase]
   ['verb-phrase]
   ['prep-phrase]
   ['art-phrase]
   ['art-phrase 'verb]
   ['verb 'prep-phrase]
   ['verb 'art-phrase]
   ['art-phrase 'verb-phrase]
   ['noun-phrase 'verb-phrase]
   ['noun-phrase 'prep-phrase]
   ['verb-phrase 'noun-phrase]
   ['verb-phrase 'prep-phrase]
   ['prep-phrase 'verb-phrase]
   ])

;; DICTIONARY ==================================================================
(def noun
  ["cat" "bat" "horse" "elephant" "explosion" "aardvark" "chair" "elbow" "person"
   "tissue" "zebra" "rock" "mountain" "computer" "alien"])

(def verb
  ["growls" "runs" "flies" "yells" "explodes" "digs" "sits" "bends" "blows" "speaks" "gallops"
   "climbs" "falls" "is"])

(def adjective
  ["fluffy" "creepy" "fast" "big" "loud" "weird" "chair-like" "bendy" "irrelevant"
   "soft" "stripey" "hard" "enormous" "electronic" "alien"])

(def article
  ["a" "the"])

(def preposition
  ["to" "towards" "with"])
;; ==============================END DICTIONARY=================================

;; Checks a given string against the "dictionary" (above) and tags it appropriately
(defn analyze-word
  [word]
  (cond
    (in? noun word) ['noun word]
    (in? verb word) ['verb word]
    (in? adjective word) ['adjective word]
    (in? article word) ['article word]
    (in? preposition word) ['preposition word]))

;; Checks a pair of tagged words and returns a phrase (like noun-phrase) if they can be combined as such
(defn analyze-phrase
  [phrase]
  (let [structure (map first phrase)
        words (map second phrase)]
    (cond
      (contains? phrase-rules structure) [[(get phrase-rules structure) (s/join " " words)]]
      :else phrase)))

;; Basically just maps analyze-word over a longer string
(defn analyze-sentence
  [inputsentence]
  (let [sentence (s/split inputsentence #" ")]
        (vec (map analyze-word sentence))))

;; Higher level analysis, looks for phrases in an word-by-word analyzed sentence
(defn analyze-structure
  [sentence]
    (loop [x 0
           result sentence]
      (let [slice 
            (if (> (+ x 2) (count result))
              (subvec result x (inc x))
              (subvec result x (+ 2 x)))]
        (if (not= slice (analyze-phrase slice))
            (if (= x (- (count result) 2))
              (vec (concat (subvec result 0 x) (analyze-phrase slice) (subvec result (+ 2 x) (count result))))
              (recur (inc x) (vec (concat (subvec result 0 x) (analyze-phrase slice) (subvec result (+ 2 x) (count result))))))
            (if (= x (dec (count result)))
              result
              (recur (inc x) result))))))

;; Runs analyze-structure until there's nothing left to analyze
(defn analyzer 
  [sentence]
  (loop
    [last ""
     thisone (analyze-structure (analyze-sentence sentence))]
    (if (= thisone last)
      thisone
      (recur thisone (analyze-structure thisone)))))
      
;; Is input a valid english sentence?
;; based on order of words and the rules given at the top of the program
(defn check-sentence
  [inputsentence]
  (let [sentence (analyzer inputsentence)
        structure (vec (map first sentence))]
    (loop [x 0
           result []]
      (let [slice 
            (if (< x (dec (count structure)))
              (subvec structure x (+ 2 x))
              (subvec structure x (inc x)))]
        (if (< x (dec (count structure)))
          (recur (inc x) (conj result (in? rules slice)))
          (every? identity (conj result (in? rules slice))))))))

;; Attempts to find an order of the given words that makes a valid sentence (one that passes check-sentence)
(defn fix-sentence
  [inputsentence]
    (if (check-sentence inputsentence)
       inputsentence
      (fix-sentence (s/join " " (shuffle (s/split inputsentence #" "))))))
