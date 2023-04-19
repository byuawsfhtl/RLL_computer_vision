powershell "Write-Host 'Folder size report generator' -ForegroundColor Green;Add-Type -AssemblyName System.Windows.Forms;Add-Type -AssemblyName System.Drawing;$testform = New-Object System.Windows.Forms.Form;$testform.Text = 'Folder size report';$testform.Size = New-Object System.Drawing.Size(300,250);$testform.StartPosition = 'CenterScreen';$okb = New-Object System.Windows.Forms.Button;$okb.Location = New-Object System.Drawing.Point(200,180);$okb.Size = New-Object System.Drawing.Size(75,25);$okb.Text = 'Ok';$okb.DialogResult = [System.Windows.Forms.DialogResult]::OK;$testform.AcceptButton = $okb;$testform.Controls.Add($okb);$lb = New-Object System.Windows.Forms.Label;$lb.Location = New-Object System.Drawing.Point(0,20);$lb.Size = New-Object System.Drawing.Size(240,20);$lb.Text = 'Starting folder:';$testform.Controls.Add($lb);$tb = New-Object System.Windows.Forms.TextBox;$tb.Location = New-Object System.Drawing.Point(10,40);$tb.Size = New-Object System.Drawing.Size(240,20);$testform.Controls.Add($tb);$2b = New-Object System.Windows.Forms.Label;$2b.Location = New-Object System.Drawing.Point(0,70);$2b.Size = New-Object System.Drawing.Size(240,20);$2b.Text = 'Output file:';$testform.Controls.Add($2b);$tb2 = New-Object System.Windows.Forms.TextBox;$tb2.Location = New-Object System.Drawing.Point(10,90);$tb2.Size = New-Object System.Drawing.Size(240,20);$testform.Controls.Add($tb2);$3b = New-Object System.Windows.Forms.Label;$3b.Location = New-Object System.Drawing.Point(0,120);$3b.Size = New-Object System.Drawing.Size(240,20);$3b.Text = 'Layers:';$testform.Controls.Add($3b);$tb3 = New-Object System.Windows.Forms.TextBox;$tb3.Location = New-Object System.Drawing.Point(10,140);$tb3.Size = New-Object System.Drawing.Size(240,20);$testform.Controls.Add($tb3);$testform.Topmost = $true;$testform.Add_Shown({$tb.Select()});$rs = $testform.ShowDialog();if ($rs -eq [System.Windows.Forms.DialogResult]::OK){$folder = $tb.Text;$save = $tb2.Text;$layersInput = [decimal]$tb3.Text;Write-Host 'Running' -ForegroundColor Green;Write-Host 'folder:', $folder;Write-Host 'save location:', $save;Write-Host 'layers:', $layersInput;function TreeSearch{$layers = $layersInput;v:;cd $folder;$q = New-Object system.collections.generic.queue[System.IO.FileSystemInfo];$q2 = New-Object System.Collections.Generic.Queue[int];foreach($dir in $(Get-ChildItem -path .\ -Directory)){try{$q.enqueue($dir); $q2.enqueue(1)}catch{Write-Host 'skipping setup on' $dir.fullname | Out-File -Append -FilePath $save}};while($q.count -gt 0){trap [System.IO.IOException]{echo 'error'; continue;}$level = $q2.dequeue();if($level -gt $layers){break}$top = $q.dequeue();$size = $null;try {$size = (Get-ChildItem -Path $top.fullName -Recurse | Measure-Object -Property length -sum).sum;if($size -eq $null){$size = 0}}catch{Write-Host 'skipping' $top.fullName;continue}Write-Host ($top.fullName, ' == ', 'folder size:', $size, ' == ', 'last access:', $dir.LastAccessTime) -Separator ' '; foreach($dir in $(Get-ChildItem -Path $top.fullName -Directory)){try{$q.enqueue($dir); $q2.enqueue($level + 1)}catch{Write-Host 'skipping adding' $dir.fullName}}}};TreeSearch 6> $save};Write-Host 'Done' -ForegroundColor Green"