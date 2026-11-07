
<# Seems to unable to use CJK character? #>

<# Configuration #>
$source = "C:\Users\pig21\Downloads\a"
$dest = "C:\Users\pig21\Downloads\b"
$dir_rex = [regex] "^([0-9][0-9][0-9])$"
$is_keep_source = 0

cd $source
$dirs = Get-ChildItem -Path $source | Where-Object {($_.Name -match $dir_rex)}
echo $dirs
$items = Get-ChildItem -Path $dirs

if ($is_keep_source) {
	foreach ($item in $items) {Copy-Item -Path $item.FullName -Destination $dest}
}
else {
	foreach ($item in $items) {Move-Item -Path $item.FullName -Destination $dest}
}
