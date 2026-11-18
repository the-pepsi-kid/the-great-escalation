"""Individual scene commissions for the remaining 104 illustrations."""
SCENES={}
for row in '''
M02|A broadcaster interviews a silhouette behind three curtains; the silhouette is itself reading a rumor from another television.
M03|An enormous mechanical newsroom sorting machine feeds tiny audience members customized portions of illustrated dread.
M04|Six self-appointed experts argue around seven microphones while a qualified technician waits outside the studio glass.
M05|A terrified family stares at a single red point on a giant outage map while their functioning room glows with electronics.
M06|A television producer physically interrupts a repair technician to insert a lavish advertisement into an emergency broadcast.
M07|A field reporter gravely points at a perfectly ordinary office parking lot, framed as if it were an archaeological catastrophe.
M08|A newspaper barricade hides a simple mundane explanation; a coin slot offers a narrow glimpse behind the sensational front page.
M09|A tiny correction occupies a remote back page of a newspaper whose front cover depicts the end of the world.
M10|An executive secretly hands over an enormous slide deck while every nearby employee openly holds a copy.
M11|A graphic designer paints flames around a photograph of a cool, unplugged server; the real computer sits harmlessly beside them.
M12|Three television crews film the same technician working on the same broken server from increasingly dramatic camera angles.
M13|A calm community radio host gives practical instructions beside a lantern while anxious neighbors gradually relax.
M14|An investigator follows a winding trail of banknotes that ends at an invoice for the investigation itself.
M15|A studio clock controls a conveyor belt of identical outraged presenters emerging from theatrical dressing rooms.
M16|A breathless editor tears down a catastrophe poster while a warehouse worker is still printing merchandise for it.
M17|A modest investigator compares a loud rumor board against a small, clear collection of physical records and receipts.
M18|A camera operator finally swivels away from a grandstanding executive and toward the technician reconnecting the network.
M19|A beautiful emergency podium, six functioning microphones, and elaborate lighting surround a visibly disconnected network rack.
M20|A public-service announcer holds a clear practical diagram while a group of sensationalist presenters waits impatiently backstage.
M21|An investigator magnifies a pixelated picture of another pixelated picture; the actual source sits unopened on the desk.
M22|An executive whispers into a colleague's ear while the giant studio microphone remains illuminated in front of them.
M23|A patient reporter works late through boxes of records while a conveyor belt of instant reactions rushes past the window.
M24|A dusty emergency television endlessly repeats an alarm in a room where the original problem was fixed days ago.
M25|A grounded local reporter watches a technician repair a real fault; a restrained camera crew lets the work happen.
D02|A motionless fleet of airplanes waits under a clear sky while an exhausted controller stares at a tiny service-token alert.
D03|A bank lobby crowds around an unavailable payment terminal while a technician follows one misplaced network cable behind the teller wall.
D04|A yellowed ancient router sits on a velvet historical pedestal, surrounded by executives afraid to touch its failing power brick.
D05|A city of working computers points toward an empty directory board, unable to locate services that are visibly still running.
D06|A cheerful engineer makes a tiny keyboard edit as a long row of production monitors changes color behind them.
D07|An imposing office security door rejects a harmless certificate because a tiny wall calendar has advanced one day.
D08|A backhoe bucket delicately and unerringly snips a lone underground fiber cable while workers study an inaccurate map.
D09|An immaculate backup vault is full of empty folders; a restoration engineer realizes the neatly maintained shelf contains nothing.
D10|An abstract cloud facility becomes an overcrowded physical operations room with overloaded consoles and distant stranded users.
D11|A training console accidentally drives a real production machine while the instructor's celebratory drill props fall to the floor.
D12|A pristine emergency generator sits beside an empty fuel gauge and a thick, confidently approved continuity binder.
D13|A queue of desperate laptops waits at an address dispenser that contains one remaining numbered ticket, rendered without readable digits.
D14|Employees hold valid badges outside a locked electronic office while a neglected directory-sync computer sleeps behind glass.
D15|A plumbing leak drips into a floor-mounted rack as a technician arrives with a ladder and an extremely unimpressed expression.
D16|An overenthusiastic maintenance operator shuts down two supposedly independent server clusters at the same moment.
D17|A cheerful green status display monitors itself while every real service console behind it is dark.
D18|An entire office's network connections narrow into a single fragile transceiver held together with a cable tie.
D19|An immense industrial process depends on a humble spreadsheet open on an abandoned beige desktop computer.
D20|A grinning deployment engineer puts on a weekend jacket as a small configuration file tumbles into a production machine.
P02|An emergency meeting expands into a second, larger boardroom while the same unresolved outage follows on a wheeled monitor.
P03|Executives unveil a ceremonial plaque on an obsolete router while its warning lights blink desperately beneath the ribbon.
P04|A robed corporate official kneels before a luminous green dashboard in an otherwise completely dark office.
P05|A fictional committee studies a single unsigned approval document under bright lamps while a witness points toward a mountain of unread binders.
P06|An executive spotlight follows a lone contractor away from the actual decision makers seated comfortably in shadow.
P07|A consultant opens a polished briefcase containing a smaller consultant who opens an even smaller briefcase.
P08|A steering wheel mounted at a committee table has many hands on it and is connected to absolutely nothing.
P09|One department's budget bucket is quietly siphoned into another while both managers smile at a shared efficiency chart.
P10|An employee finishes a cybersecurity training module while an obviously suspicious congratulatory envelope slides underneath the keyboard.
P11|A server sits on a rotating departmental handoff carousel; every manager points to the next office as alarms continue.
P12|Managers finally roll up their sleeves and help technicians lift replacement equipment into a damaged rack.
P13|A spotless approval stamp lands on meeting minutes with a conspicuous empty space where the decision should have been.
P14|A branding workshop carefully chooses catastrophe-colored swatches while an actual repair queue grows outside the room.
P15|A technician receives a crucial replacement part by bicycle courier while the enormous purchase-order machine is still warming up.
P16|A luxury concierge offers a velvet-rope entrance to a support desk while a queue of ordinary emergencies waits nearby.
P17|An austere legal adviser reaches for the mute button just as a technician begins pointing at the actual incident evidence.
P18|Employees obediently return to an office full of blank screens and disconnected desk phones, watched by a satisfied executive.
P19|An audit committee carefully squeezes a stack of accountability records into a very narrow appointment slot.
P20|Three ordinary people read, sign and implement the same clear repair document while ceremonial approval machinery gathers dust.
C02|A prophet unveils tomorrow's calendar page while an assistant wheels in a vast supply of identical future calendar pages.
C03|An enthusiast connects arbitrary clock faces, receipts and cereal shapes with red string while ignoring an obvious broken plug.
C04|A concealed informant presents an empty envelope inside several increasingly secretive locked containers.
C05|Followers solemnly carry a rolled plan that is visibly being drawn by someone walking behind the procession.
C06|A well-lit prediction studio presents a dark globe while an ordinary street outside carries on with every light working.
C07|A rumor passes through a row of increasingly old photocopiers until its final blurry image is treated as sacred evidence.
C08|A frantic investigator links a spilled coffee cup to a distant network outage with an absurdly long length of red string.
C09|An elaborate imaginary weather-control console is assembled from a desk fan, a kettle and dramatic unrelated satellite photographs.
C10|A huckster presents a flag-draped router whose ethernet cables evaporate into theatrical stage fog.
C11|A stagehand replaces an apocalypse date card with a new blank card while the prophet keeps the same triumphant pose.
C12|A whispering personality records a voice message beneath layers of blankets while a mundane visible explanation waits on the desk.
C13|An interviewer releases an endless stream of question-shaped paper while a simple answer remains trapped in a closed drawer.
C14|A self-appointed authority hides a tiny caveat inside an absurdly large locked classified binder.
C15|A confident online personality watches their fantastical forecast dissolve against an ordinary sunlit scene of people doing repairs.
H02|A composed senior engineer with worn glasses points to one simple physical diagram while a room full of argumentative managers falls silent.
H03|A technician changes one tiny directory entry and a citywide web of disconnected service lines suddenly finds its destinations.
H04|A tired technician reaches for the plain power switch while a crowd awaits an extravagantly complicated technical ritual.
H05|An engineer opens one unassuming log file while three elaborate speculative conspiracy diagrams collapse behind the monitor.
H06|A quiet night-shift team performs careful documented maintenance under a warmly lit clock, with no executives in sight.
H07|A recovery engineer restores actual files from a tested backup while untouched glossy backup reports lie in a discarded stack.
H08|A help-desk worker opens an old ticket drawer and immediately recognizes a problem that a startled executive insists is unprecedented.
H09|An analyst watches a clear stream of network packets pass through a diagnostic lens while a melodramatic rumor board blurs behind them.
H10|An engineer calmly turns a deployment mechanism backward and the old, stable configuration slides neatly into place.
H11|A field technician with a ladder and tool bag replaces a failed physical uplink beneath an enormous advertisement for cloud services.
H12|An exhausted night-shift engineer solves an outage beside a cold meal and a wall of unanswered staffing requests.
H13|A clear practical runbook is passed from an experienced worker to a new team as a lone indispensable expert finally takes a day off.
H14|A junior technician raises one thoughtful hand and points to an obvious contradiction that an entire senior meeting has overlooked.
H15|An ordinary working system quietly performs its actual purpose while the technicians enjoy an unusually undramatic cup of coffee.
W02|An executive sweeps a pile of unresolved ticket folders into a cabinet while every user behind the glass still holds broken equipment.
W03|A relaxed boardroom erupts into theatrical alarm only when the chief executive notices the already-existing outage screen.
W04|A stagehand lowers an enormous apocalypse prop to reveal a small, ordinary technical inconvenience behind it.
W05|Calm robot evidence clerks present organized receipts to an ordinary human court; a judge and counsel examine them with visible procedural care.
W06|A silent operations room and a peaceful street share a slow Saturday morning, with technicians suspiciously enjoying their breakfast.
W07|An independent reviewer studies physical evidence at a plain desk while interested executives wait outside the glass.
W08|Neighbors and technicians share tools and carry replacement equipment together without banners, sponsorships or cameras.
W09|A caravan of news cameras leaves one repaired service and rushes toward a distant new flashing light.
W10|A meeting action item slips through a growing maze of empty calendar boxes and dusty follow-up folders.
W11|A technician opens the actual incident record to everyone before a group of speechwriters can finish arranging their talking points.
W12|A bicycle courier delivers a tray of strong coffee to a night-shift operations room whose entire team visibly regains focus.
W13|A meeting presenter produces one last small folder from behind their back while the exhausted audience reaches for the door.
W14|A long-locked emergency fund cabinet finally opens for a visibly real operational emergency rather than a ceremonial executive request.
W15|Ordinary users recognize the technician who fixed their systems and call them back, passing an unused executive publicity stand.
'''.strip().splitlines():
    code,scene=row.split('|',1);SCENES['TGE-'+code]=scene
assert len(SCENES)==104
