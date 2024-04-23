./housing create

for i in {1..10}; do
    random_bedrooms=$((1 + RANDOM % 6))
    random_bathrooms=$((1 + RANDOM % 5))
    price=$($i + 300000)
    ./housing addBasics $($i + 400000) $random_bathrooms $random_bedrooms
    # ./housing addaccount $i"@gmail.com"  "user"$i
    # ./housing addpost $i" of great posts"  $i
done

# declare -a interests=("sports" "yoga" "reading" "skateboarding" "travel" "music" "shopping" "food" "gym" "food" "netflix")
# for i in "${interests[@]}"; do
#     ./face addinterest $i
# done

# for i in {1..10}; do 
#     ./face addaccountinterest $i $i
#     ./face addaccountinterest $i $(((($i + 3) % 11) + 1))
#     ./face addaccountinterest $i $(((($i + 6) % 11) + 1))
# done

# for i in {1..10}; do 
#     ./face addcomment $i $(((($i + 2) % 10) + 1)) "random text"
#     ./face addcomment $i $(((($i + 4) % 10) + 1)) "random text"
# done

