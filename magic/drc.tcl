load {PATH}/{CELL}.mag
logcommands drc/{CELL}_drc.log
select top cell
expand
view
set b [view bbox]
box values [lindex $b 0] [lindex $b 1] [lindex $b 2] [lindex $b 3]
drc style drc(full)
drc catchup
set n 0
foreach {rule pairs} [drc listall why] {
    puts "[llength $pairs] $rule"
    incr n [llength $pairs]
}
puts "Total DRC errors found: $n"
quit
