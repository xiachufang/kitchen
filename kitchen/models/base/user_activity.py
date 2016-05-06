import datetime
from peewee import DateTimeField
from kitchen.daos.base import BaseDAO
from kitchen.libs.fields import UnsignedBigIntegerField


def user_activity_base(activity):
    class UserDAO(BaseDAO):
        class Meta:
            db_table = '%s_userdao' % activity
            indexes = (
                (('user_id', 'target_id'), True),
            )

        user_id = UnsignedBigIntegerField(null=False, index=True)
        target_id = UnsignedBigIntegerField(null=False)
        sequence = DateTimeField(default=datetime.datetime.now, null=False)

    class TargetDAO(BaseDAO):
        class Meta:
            db_table = '%s_targetdao' % activity
            indexes = (
                (('target_id', 'user_id'), True),
            )

        target_id = UnsignedBigIntegerField(null=False, index=True)
        user_id = UnsignedBigIntegerField(null=False)
        sequence = DateTimeField(default=datetime.datetime.now, null=False)

    class Action(object):

        @classmethod
        def insert(cls, user_id, target_id, sequence=None):
            if not sequence:
                sequence = datetime.datetime.now()
            UserDAO.select_shard(user_id).insert(user_id=user_id, target_id=target_id, sequence=sequence).execute()
            TargetDAO.select_shard(target_id).insert(user_id=user_id, target_id=target_id, sequence=sequence).execute()

        @classmethod
        def delete(cls, user_id, target_id):
            UserDAO.select_shard(user_id).delete().where(
                UserDAO.user_id == user_id,
                UserDAO.target_id == target_id
            ).execute()
            TargetDAO.select_shard(target_id).delete().where(
                TargetDAO.user_id == user_id,
                TargetDAO.target_id == target_id
            ).execute()

        @classmethod
        def targets_by_user(cls, user_id, cursor=0, size=20):
            return list(a.user_id for a in UserDAO.select_shard(user_id).select(UserDAO.target_id).where(
                UserDAO.user_id == user_id
            ).order_by(UserDAO.sequence.desc()).limit(size).offset(cursor))

        @classmethod
        def users_by_target(cls, target_id, cursor=0, size=20):
            return list(a.user_id for a in TargetDAO.select_shard(target_id).select(TargetDAO.target_id).where(
                TargetDAO.target_id == target_id
            ).order_by(TargetDAO.sequence.desc()).limit(size).offset(cursor))

        @classmethod
        def count_targets_by_user(cls, user_id):
            return UserDAO.select_shard(user_id).select().where(
                UserDAO.user_id == user_id
            ).count()

        @classmethod
        def count_users_by_target(cls, target_id):
            return TargetDAO.select_shard(target_id).select().where(
                TargetDAO.target_id == target_id
            ).count()

        @classmethod
        def if_user_has_targets(cls, user_id, target_ids):
            collected_target_ids = UserDAO.select_shard(user_id).select(UserDAO.target_id).where(
                UserDAO.user_id._in(target_ids)
            ).execute()
            return dict((str(rid), int(rid) in collected_target_ids) for rid in target_ids)

    Action.UserDAO = UserDAO
    Action.TargetDAO = TargetDAO
    return Action
