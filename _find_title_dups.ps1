$files=Get-ChildItem -File -Filter *.html
$entries=@()
foreach($f in $files){
  $raw=[IO.File]::ReadAllText($f.FullName)
  $tm=[regex]::Match($raw,'<title>(.*?)</title>','IgnoreCase,Singleline')
  $t=if($tm.Success){$tm.Groups[1].Value.Trim()}else{''}
  $entries += [pscustomobject]@{ File=$f.Name; Title=$t }
}
$dups=$entries | Group-Object Title | Where-Object { $_.Count -gt 1 -and $_.Name -ne '' }
"DUP_GROUPS=$($dups.Count)"
foreach($g in $dups){
  "`nTITLE: $($g.Name)"
  $g.Group | ForEach-Object { " - $($_.File)" }
}