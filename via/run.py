import os

import click
import networkx as nx
import community

from via.data.builder import DatasetBuilder
from via.learn.train import Trainer
from via.learn.analyze import ProjectionAnalyzer
from via.util.util import enrich_projection_txt

@click.command()
@click.argument('params_dir')
def build_dataset(params_dir):
    process = DatasetBuilder(params_dir)
    process.run()


@click.command()
@click.argument('params_dir')
def build_projection(params_dir):
    process = Trainer(params_dir)
    process.run()


@click.command()
@click.argument('params_dir')
def run_metrics(params_dir):
    process = ProjectionAnalyzer(params_dir)
    process.run()

@click.command()
@click.argument('input_path')
def enrich_projection(input_path):
    enrich_projection_txt(input_path)


@click.command()
@click.argument('experiment_dir')
def run_louvain(experiment_dir):
    g = nx.read_edgelist(
        os.path.join(experiment_dir, 'projection.txt'),
        create_using=nx.DiGraph, data=[
            ('weight', float), ('p_prereq', float), ('p_course', float)])
    g = g.to_undirected()
    d = community.generate_dendrogram(g)
    level_0 = community.partition_at_level(d, 0)
    for i in range(max(level_0.values())):
        print('=' * 40)
        major = []
        for class_id, partition_num in level_0.items():
            if partition_num == i:
                major.append(class_id)
        print(major)
        print('=' * 40)


@click.command()
@click.argument('experiment_dir')
def run_pagerank(experiment_dir):
    year1 = year2 = year3 = year4 = set()
    year1 = {'AFRICAAM20A', 'CME100', 'EE100', 'MS&E472', 'MUSIC160', 'ORALCOMM215',
             'CS106B', 'PHYSICS41', 'TAPS124D', 'PWR1LP'
             'ENGLISH92', 'ENGR40M', 'ENGR103', 'PHYSICS43'}
    year2 = {'CS1U', 'CS92SI', 'CS107', 'FRENLANG2', 'MS&E193',
             'CS103', 'CS108', 'CS198', 'FRENLANG3',
             'CS109', 'FRENLANG21C', 'ME101', 'PWR2BA'}
    year3 = {'CME103', 'CS161', 'EARTHSYS10', 'FRENLANG22C', 'PSYC199',
             'CS110', 'CS124', 'FRENLANG20B', 'MUSIC124A'}
    year4 = {'CS148', 'CS221', 'CS229'}

    g = nx.read_edgelist(
        os.path.join(experiment_dir, 'projection.txt'),
        create_using=nx.DiGraph, data=[
            ('weight', float), ('p_prereq', float), ('p_course', float)])
    course_ids = year1 | year2 | year3 | year4
    course_ids = [node for node in g.nodes() if node in course_ids]
    ppr = {node: 1 if node in course_ids else 0.0 for node in g.nodes()}
    for cid, score in ppr.items():
        if cid in year2:
            ppr[cid] = score * 2
        if cid in year3:
            ppr[cid] = score * 4
        if cid in year4:
            ppr[cid] = score * 8
    total = sum(ppr.values())
    for cid, score in ppr.items():
        ppr[cid] /= total

    from collections import Counter
    print(Counter(ppr.values()))

    page_rank = nx.pagerank(g, alpha=0.6, personalization=ppr, weight='weight', dangling=ppr)
    scores = sorted([(page_rank.get(node, 0), node) for node in g.nodes() if node not in course_ids], reverse=True)[:10]
    for score, course_id in scores:
        print(f"{score}:\t {course_id}")


