for ((i=0; i<11; i++))
do
	cp Lambda_$i/Production_MD/md$i.xvg .
done

for (( i=1; i<10; i++ ))
do
	cp md$i.xvg $i.xvg
	python extract_lambdas.py $i.xvg 6 8
	rm $i.xvg
done

cp md0.xvg 0.xvg
python extract_lambdas.py 0.xvg 6 7
rm 0.xvg

cp md20.xvg 20.xvg
python extract_lambdas.py 20.xvg 6 7
rm 0.xvg
