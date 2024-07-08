import logging
from datetime import datetime, date, timedelta
from typing import Any
from garminworkouts.garmin.garminworkout import GarminWorkout
from garminworkouts.models.event import Event
from garminworkouts.models.note import Note
from garminworkouts.models.workout import Workout
from garminworkouts.models.settings import settings


class GarminClient(GarminWorkout):
    def get_calendar(self, date, days=7) -> tuple[list[str], list[str], dict]:
        year = str(date.year)
        month = str(date.month - 1)
        url: str = f"{GarminClient._CALENDAR_SERVICE_ENDPOINT}/year/{year}/month/{month}"
        response_jsons: dict = self.get(url).json().get('calendarItems')
        updateable_elements: list[str] = []
        checkable_elements: list[str] = []
        note_elements: dict = {}
        date_plus_days: datetime = date + timedelta(days=days)

        for item in response_jsons:
            item_date = datetime.strptime(item.get('date'), '%Y-%m-%d').date()
            item_type: Any = item.get('itemType')

            if item_type == 'workout':
                if item_date < date:
                    logging.info("Deleting workout '%s'", item.get('title'))
                    self.delete_workout(item.get('workoutId'))
                elif item_date < date_plus_days:
                    updateable_elements.append(item.get('title'))

            elif item_type == 'activity':
                payload: dict = self.get_activity_workout(item.get('id'))
                if 'workoutName' in payload:
                    checkable_elements.append(payload.get('workoutName', str))

            elif item_type == 'note':
                if item.get('trainingPlanId'):
                    payload = self.get_note(trainingplan=True, note_id=item.get('id')).json()
                else:
                    payload = self.get_note(trainingplan=False, note_id=item.get('id')).json()
                note_elements[payload.get('noteName')] = payload

        return updateable_elements, checkable_elements, note_elements

    def trainingplan_reset(self, args) -> None:
        workouts, notes, plan = settings(args)
        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in self.list_workouts()}
        for workout in workouts:
            workout_name: str = workout.get_workout_name()
            existing_workout: dict | None = existing_workouts_by_name.get(workout_name)
            if existing_workout and plan in existing_workout.get('description'):
                workout_id: str = Workout.extract_workout_id(existing_workout)
                logging.info("Deleting workout '%s'", workout_name)
                self.delete_workout(workout_id)

    def update_workouts(self, ue, workouts: list[Workout], plan: str) -> None:
        workouts_by_name: dict[str, Workout] = {w.get_workout_name(): w for w in workouts}

        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in self.list_workouts()}
        c: int = 0

        for wname in ue:
            existing_workout: dict | None = existing_workouts_by_name.get(wname)
            description: dict | None = existing_workout.get('description') if existing_workout else None
            if description and plan in description:
                workout_id: str = Workout.extract_workout_id(existing_workout)
                workout_owner_id: str = Workout.extract_workout_owner_id(existing_workout)
                workout_author: dict = Workout.extract_workout_author(existing_workout)
                workout: Workout = workouts_by_name[wname]
                payload: dict = workout.create_workout(workout_id, workout_owner_id, workout_author)
                logging.info("Updating workout '%s'", wname)
                self.update_workout(workout_id, payload)
                c += 1

        for workout in workouts:
            day_d, *_ = workout.get_workout_date()
            if date.today() <= day_d < date.today() + timedelta(weeks=2):
                workout_name: str = workout.get_workout_name()
                existing_workout = existing_workouts_by_name.get(workout_name)
                if not existing_workout:
                    payload = workout.create_workout()
                    logging.info("Creating workout '%s'", workout_name)
                    workout_id = Workout.extract_workout_id(self.save_workout(payload))
                    self.schedule_workout(workout_id, day_d.isoformat())
                    c += 1
        if c == 0:
            logging.info('No workouts to update')

    def update_notes(self, ne, notes: list[Note], plan: str) -> None:
        for note in notes:
            day_d, _, _ = note.get_note_date()
            if date.today() <= day_d < date.today() + timedelta(weeks=2):
                note_name: str = note.get_note_name()
                existing_note: dict | None = ne.get(note_name)
                if not existing_note:
                    payload: dict = note.create_note(date=day_d.isoformat())
                    logging.info("Creating note '%s'", note_name)
                    self.save_note(note=payload)
                else:
                    note_id: str | None = existing_note.get('noteId')
                    note_obj: Note = ne.get(note_name)
                    payload = note_obj.create_note(note_id)
                    logging.info("Updating note '%s'", note_name)
                    if existing_note.get('trainingPlanId'):
                        self.update_note(note_id=note_id, note=payload)
                        self.save_note(note=payload)
                    else:
                        self.update_note(note_id=note_id, note=payload)
                        self.save_note(note=payload)

    def update_events(self, events) -> None:
        c: int = 0
        existing_events_by_name: dict = {Event.extract_event_name(w): w for w in self.list_events()}
        existing_workouts_by_name: dict = {Workout.extract_workout_name(w): w for w in self.list_workouts()}

        for event in events:
            if event.date >= date.today():
                existing_event: dict | None = existing_events_by_name.get(event.name)
                existing_workout: dict | None = existing_workouts_by_name.get(event.name)
                workout_id: str | None = Workout.extract_workout_id(existing_workout) if existing_workout else None

                if existing_event:
                    if event.date < date.today() + timedelta(weeks=1):
                        event_id: str = Event.extract_event_id(existing_event)
                        payload: dict = event.create_event(event_id, workout_id)
                        logging.info("Updating event '%s'", event.name)
                        self.update_event(event_id, payload)
                        c += 1
                else:
                    payload = event.create_event(workout_id=workout_id)
                    logging.info("Creating event '%s'", event.name)
                    self.save_event(payload)
                    c += 1
        if c == 0:
            logging.info('No events to update')
