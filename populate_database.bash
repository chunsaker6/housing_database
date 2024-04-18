./face create

for i in {1..10}; do
    ./face adduser $i"@gmail.com"
    ./face addaccount $i"@gmail.com"  "user"$i
    ./face addpost $i" of great posts"  $i
done

declare -a interests=("sports" "yoga" "reading" "skateboarding" "travel" "music" "shopping" "food" "gym" "food" "netflix")
for i in "${interests[@]}"; do
    ./face addinterest $i
done

for i in {1..10}; do 
    ./face addaccountinterest $i $i
    ./face addaccountinterest $i $(((($i + 3) % 11) + 1))
    ./face addaccountinterest $i $(((($i + 6) % 11) + 1))
done

for i in {1..10}; do 
    ./face addcomment $i $(((($i + 2) % 10) + 1)) "random text"
    ./face addcomment $i $(((($i + 4) % 10) + 1)) "random text"
done

