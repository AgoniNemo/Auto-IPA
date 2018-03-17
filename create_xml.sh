#! /bin/bash

outfile=ExportOptionsPlist.plist
tabs=0

put(){
 echo '<'${*}'>' >> $outfile
}

put_head(){
 put '?'${1}'?'
}

out_tabs(){
 tmp=0
 tabsstr=""
 while [ $tmp -lt $((tabs)) ]
 do
  tabsstr=${tabsstr}'\t'
  tmp=$((tmp+1))
 done
 echo -e -n $tabsstr >> $outfile
}

put_key(){
    out_tabs
    echo '<'${1}'>'${2}'</'${1}'>' >> $outfile
}

tag_start(){
 out_tabs
 put $1
 tabs=$((tabs+1))
}

tag_end(){
 tabs=$((tabs-1))
 out_tabs
 put '/'${1}
}

tag_value(){
 out_tabs
 str=""
 value=""
 if [ ${#2} -gt 0 ]
 then
    value=' value="'${2}'"'
 fi
 str=${1}${value}'/'
 put $str
}