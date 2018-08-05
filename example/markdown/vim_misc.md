## Workflow to disable feature in SvC

* `:Ag disabledFeatures`, <c-a> (alles markieren), <c-q> (ins quickfix verschieben)
* Makro aufnehmen, bswp. ins register "a
* cdo !normal @a
	* cdo: Führe folgende Befehle auf die Items in der QuickFixList aus
	* !normal sagt in welchem Modus folgende Zeichena eingetippt werden

## How to vimgrep multiple files

* Ag the files you want to search through
* Add the buffers to the arglist: `:bufdo argadd #`
* Grep the arglist e.g. for *Target*, case sensitive: `:vim /\C/Target/##`

Or

* ``:args `ag -l -G '\.proto$'` ``
* `:vim /\C/Target/##`

## Change current dir to buffers parent

`:cd %:p:h`

## Execute currentline in external command

`exec 'read !python3 -c '.shellescape(getline('.'))`

## Execute whole buffer in external commmand

`exec 'read !bash -c '.shellescape(join(getline(1,'$'), "\n"))`
