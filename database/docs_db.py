from www      import config
from database import db

def paginateDocs(lvl1,lvl2,lvl3,lvl4,lvl5,lvl6,page=1) -> dict:
    page = int(page) - 1 # adjust for pagination offest to start from 1
    like_str = ''
    if lvl1:
        like_str = f'{lvl1}'
    if lvl2:
        like_str += f'/{lvl2}'
    if lvl3:
        like_str += f'/{lvl3}'
    if lvl4:
        like_str += f'/{lvl4}'
    if lvl5:
        like_str += f'/{lvl5}'
    if lvl6:
        like_str += f'/{lvl6}'
    
    like_str += '%'

    sql = f'''
        SELECT * FROM doc_files f
        WHERE f.file_path like '{ like_str }'
        ORDER BY f.file_path
    '''
    file_paths_query = db.query(sql)
    file_paths = [x.get('file_path') for x in file_paths_query ]
    file_ids = [ x.get('file_id') for x in file_paths_query ] 

    # Filepaths 
    sql = f'''
        SELECT * FROM doc_files f
        ORDER BY f.file_path
    '''
    nav_list = db.query(sql)

    # Classes
    sql = f'''
        SELECT c.*, f.file_path
        FROM doc_classes c
        JOIN doc_files f ON c.file_id = f.file_id
        WHERE c.file_id IN ('{ "','".join([ str(x) for x in file_ids]) }')
        ORDER BY c.name    
    '''
    classes = db.query(sql)

    # Routes
    sql = f'''
        SELECT *
        FROM doc_routes r
        JOIN doc_files f ON r.file_id = f.file_id
        WHERE r.file_id IN ('{ "','".join([ str(x) for x in file_ids]) }')
        ORDER BY r.url    
    '''
    routes = db.query(sql)


    # imports
    sql = f'''
        SELECT *
        FROM doc_dependencies d
        JOIN doc_files f ON d.file_id = f.file_id
        WHERE d.file_id IN ('{ "','".join([ str(x) for x in file_ids]) }')
        ORDER BY d.module, d.object    
    '''
    imports = db.query(sql)

    # Class methods 
    sql = f'''
        SELECT f.*, fi.file_path
        FROM doc_functions f
        JOIN doc_files fi ON f.file_id = fi.file_id
        WHERE f.file_id IN ('{ "','".join([ str(x) for x in file_ids]) }')   
        AND f.class_id IS NOT NULL
        AND LEFT(f.name, 1) <> '_'
        ORDER BY f.name
    '''
    methods = db.query(sql)
    
    # Functions 
    sql = f'''
        SELECT f.*, fi.file_path
        FROM doc_functions f
        JOIN doc_files fi ON f.file_id = fi.file_id
        WHERE f.file_id IN ('{ "','".join([ str(x) for x in file_ids]) }')  
        AND f.class_id IS NULL
        AND LEFT(f.name, 1) <> '_'
        ORDER BY f.name
    '''
    functions = db.query(sql)

    return { 'file_path': file_paths, 'nav_list': nav_list, 'classes': classes, 'class_funcs': methods, 'functions': functions, 'routes': routes, 'imports': imports}

def paginateImportDependancies() -> dict:
    ''' Does not paginate. Displays all on one page '''

    sql = f'''
        SELECT 
            f.file_path
            ,SUM(CASE WHEN SUBSTRING(d.module, 1, 3) = 'app' THEN 1 ELSE 0 END ) as app
            ,SUM(CASE WHEN SUBSTRING(d.module, 1, 11) = 'app.modules' THEN 1 ELSE 0 END ) as app_modules
            ,SUM(CASE WHEN SUBSTRING(d.module, 1, 9) = 'app.views' THEN 1 ELSE 0 END ) as app_views
            ,SUM(CASE WHEN SUBSTRING(d.module, 1, 17) = 'environment' THEN 1 ELSE 0 END ) as environment 
            ,SUM(CASE WHEN SUBSTRING(d.module, 1, 8) = 'database' THEN 1 ELSE 0 END ) as database 
            ,SUM(CASE WHEN SUBSTRING(d.module, 1, 4) = 'docs' THEN 1 ELSE 0 END ) as docs 
            ,SUM(CASE WHEN SUBSTRING(d.module, 1, 7) = 'modules' THEN 1 ELSE 0 END ) as modules 
        FROM doc_dependencies d
        JOIN doc_files f ON d.file_id = f.file_id
        WHERE REPLACE(d.module, '.', '/') || '/' IN ( 
            SELECT f.file_path FROM doc_folders f
        )
        OR 
        REPLACE(SUBSTRING(d.module, 1, length(d.module) - position('.' in reverse_string(d.module))), '.', '/') || '/' IN (
            SELECT f.file_path FROM doc_folders f
            )
        GROUP BY f.file_path
        ORDER BY f.file_path
    '''
    internal_dependencies = db.query(sql)

    sql = f'''
        SELECT *
        FROM doc_dependencies d
        JOIN doc_files f ON d.file_id = f.file_id
        WHERE REPLACE(d.module, '.', '/') || '/' NOT IN ( 
            SELECT f.file_path FROM doc_folders f
        )
        AND 
        REPLACE(SUBSTRING(d.module, 1, length(d.module) - position('.' in reverse_string(d.module))), '.', '/') || '/' NOT IN (
            SELECT f.file_path FROM doc_folders f
            )

        ORDER BY f.file_path;
    '''
    external_dependencies = db.query(sql)

    return { 'internal': internal_dependencies, 'external': external_dependencies }

def paginateRoutes() -> dict:
    ''' Does not paginate. Displays all on one page '''
    sql = f'''
        SELECT r.url, r.permissions, r.methods, f.file_path
        FROM doc_routes r
        JOIN doc_files f ON r.file_id = f.file_id
        ORDER BY r.url;
    '''
    query = db.query(sql)
    return {'results': query}

def paginateStats() -> dict:
    ''' Does not paginate. Displays all on one page '''
    sql = f'''
        SELECT count(*) as total_files
            ,SUM(CASE WHEN f.ext = 'css' THEN 1 ELSE 0 END) AS css_files
            ,SUM(CASE WHEN f.ext = 'js' THEN 1 ELSE 0 END) AS js_files
            ,SUM(CASE WHEN f.ext = 'py' THEN 1 ELSE 0 END) AS py_files
            ,SUM(CASE WHEN f.ext = 'sh' THEN 1 ELSE 0 END) AS sh_files
            ,SUM(CASE WHEN f.ext = 'sql' THEN 1 ELSE 0 END) AS sql_files
            ,sum(f.lines) as total_lines
            ,SUM(CASE WHEN f.ext = 'css' THEN f.lines ELSE 0 END) AS css_lines
            ,SUM(CASE WHEN f.ext = 'js' THEN f.lines ELSE 0 END) AS js_lines
            ,SUM(CASE WHEN f.ext = 'py' THEN f.lines ELSE 0 END) AS py_lines
            ,SUM(CASE WHEN f.ext = 'sh' THEN f.lines ELSE 0 END) AS sh_lines
            ,SUM(CASE WHEN f.ext = 'sql' THEN f.lines ELSE 0 END) AS sql_lines
        FROM doc_files f
    '''
    summary = db.queryOne(sql)

    sql = f'''
        SELECT *
        FROM doc_files f
        ORDER BY f.file_path
    '''
    file_list = db.query(sql)

    return {'summary': summary, 'detail': file_list}

def dropAllDocs() -> bool:
    ''' When rebuilding the documentation we dont want to keep the old '''
    tables = ['doc_routes', 'doc_functions', 'doc_classes', 'doc_dependencies', 'doc_folders', 'doc_files']
    for table in tables:
        sql = f'DELETE FROM { table } WHERE 1=1;'
        db.execute(sql)
    return True


def getDocFolderIdFromFilePath(file_path):
    file_path = file_path.split('/')
    file_path.pop()
    file_path = '/'.join(file_path) + '/'

    sql = f'''
        SELECT f.folder_id 
        FROM doc_folders f
        WHERE f.file_path = '{ file_path }'
    '''

    return db.scalar(sql)

def getDocFileIdFromFilePath(file_path):
    folder_id = getDocFolderIdFromFilePath(file_path) 
    name = file_path
    name = name.split('/').pop()

    sql = f'''
        SELECT f.file_id 
        FROM doc_files f
        WHERE f.folder_id = '{ folder_id }'
        AND f.name = '{ name }'
    '''
    return db.scalar(sql)

def updateDocRoutesDb(routes) -> bool:
    ''' Adds to the documentation for routes '''
    for link in routes:
        file_path = link.get('file_path')
        permissions = link.get('permissions')

        for url in link.get('route'):
            route_dbo = {
                'file_id'      : getDocFileIdFromFilePath(file_path)
                ,'methods'     : ", ".join(url.get('methods',[]))
                ,'permissions' : permissions
                ,'url'         : url.get('url')
            }

            db.upsert(route_dbo)
            
    db.commit()
    return True

def updateDocClassesDb(classes) -> bool:
    ''' Adds to the documentation for classes '''
    try:
        for cls in classes:
            class_id  = db.nextId(table='doc_classes')
            class_dbo = {
                'class_id'    : class_id
                ,'file_id'    : getDocFileIdFromFilePath(cls.get('file_path'))
                ,'name'       : cls.get('name')
                ,'superclass' : ", ".join(cls.get('superclass',[]))
                ,'docstring'  : cls.get('docstring')
                ,'parameters' : cls.get('parameters')
            }
            
            db.add(class_dbo)
            for func in cls.get('methods'):
                func_id = db.nextId(table='doc_functions')
                func_dbo = {
                    'function_id' : func_id
                    ,'class_id'   : class_id
                    ,'file_id'    : getDocFileIdFromFilePath(func.get('file_path'))
                    ,'name'       : func.get('name')
                    ,'returns'    : func.get('returns')
                    ,'docstring'  : func.get('docstring')
                    ,'parameters' : func.get('parameters')
                }
                db.add(func_dbo)
        db.commit()
        return True
    except Exception as e:
        return False

def updateDocFilesDb(file_paths) -> bool:
    for id, fp in enumerate(file_paths):
        folder_id = getDocFolderIdFromFilePath(fp)
        ext = fp

        # in case there is no extension
        if ext.find('.') == -1:
            ext = ''
        else:
            while ext.find('.') != -1:
                ext = ext[ext.find('.')+1:]

        lines = 0
        with open(fp, 'r') as file:
            lines = len(file.readlines())

        file_dbo = {
            'file_id' : id
            ,'folder_id' : folder_id
            ,'name'  : fp.split('/').pop()
            ,'file_path' : fp
            ,'ext'   : ext
            ,'lines' : lines
        }
        
        db.add(file_dbo)
        db.commit()

def updateDocFunctionsDb(functions) -> bool:
    ''' Adds to the documentation for functions '''
    try:
        for func in functions:
            func_id = db.nextId(table='doc_functions')
            func_dbo = {
                'function_id' : func_id
                ,'class_id'   : None
                ,'file_id'    : getDocFileIdFromFilePath(func.get('file_path'))
                ,'name'       : func.get('name')
                ,'returns'    : func.get('returns')
                ,'docstring'  : func.get('docstring')
                ,'parameters' : func.get('parameters')
            }
            
            db.add(func_dbo)
        db.commit()
        return True
    except Exception as e:
        return False

def updateDocFolderDb(folders) -> bool:
    ''' Adds to the documentation for functions '''
    try:
        root_id = 0
        for folder in folders:
            split_fp = folder.get('split_file_path')
            # This is / and it has no split file path
            if len(split_fp) == 0:
                parent_id = None
                root_id = folder.get('folder_id')
            # This catches all top level folders
            elif len(split_fp) == 1:
                parent_id = root_id
            # The parents should all be in place now we 
            else:
                folder_path = '/'.join(split_fp[:-1]) + '/'
                sql = f'''
                    SELECT * 
                    FROM doc_folders f
                    WHERE f.file_path = { folder_path }
                '''
                parent_path = db.queryOne(sql)
                
                if parent_path:
                    parent_id = parent_path.get('folder_id')

            # Name the root folder
            if len(split_fp) >= 1:
                name = split_fp[-1]
            else:
                name = '/'

            func_dbo = {
                'folder_id'   : folder.get('folder_id')
                ,'parent_id'  : parent_id
                ,'file_path'  : folder.get('file_path') if folder.get('file_path') != '' else '/'
                ,'name'       : name
            }
            db.add(func_dbo)
            db.commit()


        return True
    except Exception as e:
        db.session.rollback()
        return False

def updateDocDependencyDb(depenancies) -> bool:
    ''' Adds to the documentation for dependencies '''
    try:
        for dep in depenancies:
            if len(dep.get('objects')) > 0:
                for obj in dep.get('objects'):
                    depencancy_dbo = {
                        'file_id' : getDocFileIdFromFilePath(dep.get('file_path'))
                        ,'module' : dep.get('module')
                        ,'object' : obj
                    }
                    db.add(depencancy_dbo)
            else:
                depencancy_dbo = {
                    'file_id' : getDocFileIdFromFilePath(dep.get('file_path'))
                    ,'module' : dep.get('module')
                }
                db.add(depencancy_dbo)                
        db.commit()
        return True
    except Exception as e:
        return False