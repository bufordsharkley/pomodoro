import datetime
import unittest

import base


class PomodoroStateTests(unittest.TestCase):

  def testAdvancingWorks(self):
    for state in (base.STATES.live, base.STATES.notwork, base.STATES.nagging):
      pom = base.PomodoroState(state=state,
                               seconds=73)
      pom = base.advance_state(pom, seconds=3)
      self.assertEqual(pom.state, state)
      self.assertEqual(pom.seconds, 70,
                       'Advance did not work for ' + str(state))

  def testAdvancingNotWorkWorks(self):
    pom = base.PomodoroState(state=base.STATES.notwork,
                             seconds=73)
    pom = base.advance_state(pom, seconds=3)
    self.assertEqual(pom.seconds, 70)
    self.assertEqual(pom.state, base.STATES.notwork)

  def testTimeRunningDownEmitsRing(self):
    pom = base.PomodoroState(state=base.STATES.live,
                             seconds=60)
    with self.assertRaises(base.Ring):
      base.advance_state(pom, seconds=60)

  def testTimeRunningDownInNotWorkEmitsEnnui(self):
    pom = base.PomodoroState(state=base.STATES.notwork,
                             seconds=60)
    with self.assertRaises(base.Ennui):
      base.advance_state(pom, seconds=60)

  def testTimeRunningDownEmitsRingIfOvershot(self):
    pom = base.PomodoroState(state=base.STATES.live,
                             seconds=60)
    with self.assertRaises(base.Ring):
      base.advance_state(pom, seconds=61)

  def testAdvancingDoesntAffectUntickingPomodoro(self):
    pom = base.PomodoroState(state=base.STATES.sleep,
                             seconds=0)
    new_pom = base.advance_state(pom, seconds=3)
    self.assertEqual(pom, new_pom)

  def testWindUpCreatesProperState(self):
    pom = base.wind_up(minutes=23)
    self.assertEqual(pom.state, base.STATES.live)
    self.assertEqual(pom.seconds, 23 * 60)

  def testWindUpAlsoWorksWithSeconds(self):
    pom = base.wind_up(seconds=5)
    self.assertEqual(pom.seconds, 5)
    pom = base.wind_up(seconds=5, minutes=2)
    self.assertEqual(pom.seconds, 125)

  def testWindUpAlsoWorksWithSeconds(self):
    pom = base.wind_up(seconds=5)
    self.assertEqual(pom.seconds, 5)
    pom = base.wind_up(seconds=5, minutes=2)


class PomodoroAlignmentTests(unittest.TestCase):

  def testAlignmentForNormalCase(self):
    dt = datetime.datetime(1985, 9, 4, 11, 25)
    seconds = base.seconds_til_next_alignment(dt, alignment=0)
    self.assertEqual(seconds, 5 * 60)

  def testAlignmentForNormalCasePastHalfHour(self):
    dt = datetime.datetime(1985, 9, 4, 11, 55)
    seconds = base.seconds_til_next_alignment(dt, alignment=0)
    self.assertEqual(seconds, 5 * 60)

  def testAlignmentForImperfectAlignment(self):
    dt = datetime.datetime(1985, 9, 4, 11, 25)
    seconds = base.seconds_til_next_alignment(dt, alignment=1)
    self.assertEqual(seconds, 6 * 60)


class PomodoroObjectTests(unittest.TestCase):

  """Tests for the pomodoro object; alignment, etc"""

  def testAlignmentWorksAsExpected(self):
    self.assertEqual(base.align(23, 0), 23)
    self.assertEqual(base.align(43, 0), 13)
    self.assertEqual(base.align(23, 10), 13)
    self.assertEqual(base.align(43, 10), 3)
    self.assertEqual(base.align(5, 10), 25)

  def testDefaultAlignmentIsZero(self):
    pom = base.Pomodoro()
    self.assertEqual(pom.alignment, 0)

  def testDefaultStateIsSleep(self):
    pom = base.Pomodoro()
    self.assertEqual(pom.state.state, base.STATES.sleep)

  def testDefaultLogIsEmpty(self):
    pom = base.Pomodoro()
    self.assertEqual(pom.log, [])


class PomodoroTests(unittest.TestCase):

  def testCalculateWorkMinutesRightAway(self):
    seconds = 30 * 60
    work_minutes = base.calculate_work_minutes(seconds)
    self.assertEqual(work_minutes, 23)

  def testCalculateWorkMinutesAtTwoMinutesIn(self):
    seconds = 28 * 60
    work_minutes = base.calculate_work_minutes(seconds)
    self.assertEqual(work_minutes, 28)

  def testCalculateWorkMinutesAtOneMinuteIn(self):
    seconds = 29 * 60
    work_minutes = base.calculate_work_minutes(seconds)
    self.assertEqual(work_minutes, 25.5)

if __name__ == "__main__":
  unittest.main()
