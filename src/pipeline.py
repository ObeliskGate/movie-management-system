from src.init import db, app
from src.models import MovieInfo, ActorInfo, DirectorInfo, ProductionCompany, RoleInfo, MovieDirectorRelation
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import and_

# 通用安全删除函数
def safe_delete(entity, id_value, id_field='id'):
    """安全删除实体，处理外键约束和关系表"""
    try:
        filter_condition = {id_field: id_value}
        record = entity.query.filter_by(**filter_condition).first()
        
        if not record:
            return False, f"未找到ID为 {id_value} 的记录"
        
        # 如果是电影，先清除关系表中的关联记录
        if isinstance(record, MovieInfo):
            # 清除演员关系
            record.actors = []
            # 清除导演关系
            record.directors = []
            db.session.commit()
        
        # 如果是演员或导演，关系表会自动处理（外键约束）
        db.session.delete(record)
        db.session.commit()
        return True, f"成功删除ID为 {id_value} 的记录"
    except IntegrityError as e:
        db.session.rollback()
        app.logger.error(f"删除失败（外键约束）: {str(e)}")
        return False, "删除失败：存在关联数据，请先删除关联记录"
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"数据库错误: {str(e)}")
        return False, f"删除失败：数据库错误 - {str(e)}"

# 电影管道函数
def movie_search_pipeline(form):
    """电影搜索管道"""
    query = MovieInfo.query
    
    if form.movie_id.data:
        query = query.filter(MovieInfo.movie_id == form.movie_id.data)
    if form.movie_name.data:
        query = query.filter(MovieInfo.movie_name.ilike(f'%{form.movie_name.data}%'))
    if form.country.data:
        query = query.filter(MovieInfo.country.ilike(f'%{form.country.data}%'))
    if form.type.data:
        query = query.filter(MovieInfo.type.ilike(f'%{form.type.data}%'))
    if form.company_id.data:
        query = query.filter(MovieInfo.company_id == form.company_id.data)
    
    return query.all()

def movie_add_pipeline(form):
    """添加电影管道（包含演员和导演关系处理）"""
    try:
        # 创建电影对象
        new_movie = MovieInfo(
            movie_name=form.movie_name.data,
            release_date=form.release_date.data,
            country=form.country.data,
            type=form.type.data,
            year=form.release_date.data.year,
            company_id=form.company_id.data
        )
        
        # 安全处理演员关系（可选）
        actor_ids = form.actor_ids.data if hasattr(form, 'actor_ids') and form.actor_ids.data else None
        if actor_ids:
            actor_ids = [int(id.strip()) for id in actor_ids.split(',') if id.strip()]
            for actor_id in actor_ids:
                actor = ActorInfo.query.get(actor_id)
                if not actor:
                    return False, f"演员ID {actor_id} 不存在"
                new_movie.actors.append(actor)
        
        # 安全处理导演关系（可选）
        director_ids = form.director_ids.data if hasattr(form, 'director_ids') and form.director_ids.data else None
        if director_ids:
            director_ids = [int(id.strip()) for id in director_ids.split(',') if id.strip()]
            for director_id in director_ids:
                director = DirectorInfo.query.get(director_id)
                if not director:
                    return False, f"导演ID {director_id} 不存在"
                new_movie.directors.append(director)
        
        db.session.add(new_movie)
        db.session.commit()
        return True, f'成功添加电影 {new_movie.movie_name} (ID:{new_movie.movie_id})'
    except IntegrityError:
        db.session.rollback()
        return False, "添加失败：ID重复或数据冲突"
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"数据库错误: {str(e)}")
        return False, f"添加失败：数据库错误 - {str(e)}"
    except ValueError:
        db.session.rollback()
        return False, "ID格式错误：请使用逗号分隔的数字ID"

# 演员管道函数
def actor_search_pipeline(form):
    """演员搜索管道"""
    filters = []
    
    if form.actor_id.data:
        filters.append(ActorInfo.actor_id == form.actor_id.data)
    if form.actor_name.data:
        filters.append(ActorInfo.actor_name.ilike(f'%{form.actor_name.data}%'))
    # 修改点：gender 改为 type
    if form.type.data:
        filters.append(ActorInfo.type == form.type.data)
    if form.country.data:
        filters.append(ActorInfo.country.ilike(f'%{form.country.data}%'))
    
    return ActorInfo.query.filter(and_(*filters)).all() if filters else ActorInfo.query.all()

def actor_add_pipeline(form):
    """添加演员管道"""
    try:
        new_actor = ActorInfo(
            actor_name=form.actor_name.data,
            # 修改点：gender 改为 type
            type=form.type.data,  # 使用类型字段
            country=form.country.data,
        )
        db.session.add(new_actor)
        db.session.commit()
        return True, f'成功添加演员 {new_actor.actor_name} (ID:{new_actor.actor_id})'
    except IntegrityError:
        db.session.rollback()
        return False, "添加失败：ID重复或数据冲突"
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"数据库错误: {str(e)}")
        return False, f"添加失败：数据库错误 - {str(e)}"

# 导演管道函数
def director_search_pipeline(form):
    """导演搜索管道"""
    filters = []
    
    if form.director_id.data:
        filters.append(DirectorInfo.director_id == form.director_id.data)
    if form.director_name.data:
        filters.append(DirectorInfo.director_name.ilike(f'%{form.director_name.data}%'))
    if form.gender.data:
        filters.append(DirectorInfo.gender == form.gender.data)
    if form.country.data:
        filters.append(DirectorInfo.country.ilike(f'%{form.country.data}%'))
    
    return DirectorInfo.query.filter(and_(*filters)).all() if filters else DirectorInfo.query.all()

def director_add_pipeline(form):
    """添加导演管道"""
    try:
        new_director = DirectorInfo(
            director_name=form.director_name.data,
            gender=form.gender.data,
            country=form.country.data,
        )
        db.session.add(new_director)
        db.session.commit()
        return True, f'成功添加导演 {new_director.director_name} (ID:{new_director.director_id})'
    except IntegrityError:
        db.session.rollback()
        return False, "添加失败：ID重复或数据冲突"
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"数据库错误: {str(e)}")
        return False, f"添加失败：数据库错误 - {str(e)}"

# 出品公司管道函数
def company_search_pipeline(form):
    """出品公司搜索管道"""
    filters = []
    
    if form.company_id.data:
        filters.append(ProductionCompany.company_id == form.company_id.data)
    if form.company_name.data:
        filters.append(ProductionCompany.company_name.ilike(f'%{form.company_name.data}%'))
    if form.city.data:
        filters.append(ProductionCompany.city.ilike(f'%{form.city.data}%'))
    
    return ProductionCompany.query.filter(and_(*filters)).all() if filters else ProductionCompany.query.all()

def company_add_pipeline(form):
    """添加出品公司管道"""
    try:
        new_company = ProductionCompany(
            company_name=form.company_name.data,
            city=form.city.data,
        )
        db.session.add(new_company)
        db.session.commit()
        return True, f'成功添加出品公司 {new_company.company_name} (ID:{new_company.company_id})'
    except IntegrityError:
        db.session.rollback()
        return False, "添加失败：ID重复或数据冲突"
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"数据库错误: {str(e)}")
        return False, f"添加失败：数据库错误 - {str(e)}"

# 角色管道函数
def role_search_pipeline(form):
    """角色搜索管道"""
    filters = []
    
    if form.role_id.data:
        filters.append(RoleInfo.role_id == form.role_id.data)
    if form.movie_id.data:
        filters.append(RoleInfo.movie_id == form.movie_id.data)
    if form.actor_id.data:
        filters.append(RoleInfo.actor_id == form.actor_id.data)
    if form.role_name.data:
        filters.append(RoleInfo.role_name.ilike(f'%{form.role_name.data}%'))
    
    return RoleInfo.query.filter(and_(*filters)).all() if filters else RoleInfo.query.all()

def role_add_pipeline(form):
    """添加角色管道"""
    try:
        # 检查电影和演员是否存在
        movie = MovieInfo.query.get(form.movie_id.data)
        actor = ActorInfo.query.get(form.actor_id.data)
        
        if not movie:
            return False, f"电影ID {form.movie_id.data} 不存在"
        if not actor:
            return False, f"演员ID {form.actor_id.data} 不存在"
        
        new_role = RoleInfo(
            movie_id=form.movie_id.data,
            actor_id=form.actor_id.data,
            role_name=form.role_name.data,
        )
        db.session.add(new_role)
        db.session.commit()
        return True, f'成功添加角色 {new_role.role_name} (ID:{new_role.role_id})'
    except IntegrityError:
        db.session.rollback()
        return False, "添加失败：ID重复或关系已存在"
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"数据库错误: {str(e)}")
        return False, f"添加失败：数据库错误 - {str(e)}"

# 查询功能管道
def director_movies_pipeline(director_id):
    """查询导演执导的电影（使用新关系表）"""
    director = DirectorInfo.query.get(director_id)
    if not director:
        return None
    
    # 直接获取导演执导的电影
    return [{
        'movie_id': movie.movie_id,
        'movie_name': movie.movie_name,
        'release_date': movie.release_date
    } for movie in director.movies]

def actor_movies_pipeline(actor_id):
    """查询演员出演的电影（使用新关系表）"""
    actor = ActorInfo.query.get(actor_id)
    if not actor:
        return None
    
    # 直接获取演员出演的电影
    return [{
        'movie_id': movie.movie_id,
        'movie_name': movie.movie_name,
        'release_date': movie.release_date
    } for movie in actor.movies]

def role_info_pipeline(role_id):
    """查询角色详细信息"""
    return RoleInfo.query.get(role_id)