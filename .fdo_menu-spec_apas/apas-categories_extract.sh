#!/bin/sh
set -ufeC  # "-u" (error when using uninitialised variables),
# "-f" (disable pathname expansion), "-e" (exit on any error)
# and "-C" (no-clobber / -overwrite).

# $1 is output file name
outfile="$1"
shift
# $2 to $N are the input file names
for infile in "$@"
do
  if [ "${infile#apas0}" != "$infile" ]
  then instxt="Must also be categorised as "
  else instxt=""
  fi
  while IFS= read -r line || [ -n "$line" ]
  do
    i="$(printf %s "$line" | cut -f 1)"
    j="$(printf %s "$i" | tr '[:upper:]' '[:lower:]')"
    k="$(printf %s "$line" | cut -s -f 2)"
    if [ -n "$k" ]
    then
      if [ -n "$(printf %s "$k" | tr -d '[:blank:]')" ]
      then k="  # $k"
      else k=""
      fi
    fi 
    l="$(printf %s "$line" | cut -s -f 3)"
    if [ -n "$l" ]
    then
      if [ -n "$(printf %s "$l" | tr -d '[:blank:]')" ]
      then
        l=" $instxt${l}."
        if [ -z "$k" ]
        then k="  #"
        else k="${k}. "
        fi
      else l=""
      fi
    fi 
    printf '%s\n' "    $j = \"$i\"$k$l" >>"$outfile"
  done < "$infile"
done
