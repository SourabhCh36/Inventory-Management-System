#ISSUE INDENTS

from app import app
from auth_routes import role_required
from extension import db
from model import MaterialList,Issue_Material
from flask import Flask, redirect,render_template,request,url_for,flash


@app.route('/Issue_Materials')
@role_required(['admin','indent_user'])
def issue_materials():
    issues = Issue_Material.query.all()
    return render_template('issue_materials/list.html', issues=issues)

@app.route('/issue_materials/add', methods=['GET', 'POST'])
@role_required(['admin','indent_user'])
def add_issues():
    if request.method== 'POST':
        issues= Issue_Material(
            material_id=request.form['material_id'],
            issued_to=request.form.get('issued_to'),
            issue_date=request.form.get('issue_date'),
            quantity=request.form['quantity'],
            remarks=request.form.get('remarks', '')
        )
        db.session.add(issues)
        db.session.commit()
        flash('Material issued successfully!', 'success')
        return redirect(url_for('issue_materials'))
    materials=MaterialList.query.all()
    return render_template('issue_materials/add.html', materials=materials)

@app.route('/issue_materials/edit/<int:issue_id>', methods=['GET', 'POST'])
@role_required(['admin','indent_user'])
def edit_issue(issue_id):
    issue = Issue_Material.query.get_or_404(issue_id)
    if request.method == 'POST':
        issue.material_id = request.form['material_id']
        issue.issued_to = request.form.get('issued_to', '')
        issue.issue_date = request.form.get('issue_date')
        issue.quantity = request.form['quantity']
        issue.remarks = request.form.get('remarks', '')

        db.session.commit()
        flash('Material issued updated successfully!', 'success')
        return redirect(url_for('issue_materials'))
    
    materials = MaterialList.query.all()
    return render_template('issue_materials/edit.html', issue=issue, materials=materials)

@app.route('/issue_materials/delete/<int:issue_id>')
@role_required(['admin','indent_user'])
def delete_issue(issue_id):
    issue = Issue_Material.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    flash('Material issued deleted successfully!', 'success')
    return redirect(url_for('issue_materials'))