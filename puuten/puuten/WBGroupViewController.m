//
//  WBGroupViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-12.
//
//

#import "WBGroupViewController.h"
#import "WBViewController.h"
@interface WBGroupViewController ()

@end

@implementation WBGroupViewController
@synthesize wb_id = _wb_id;

- (void)setWb_id:(int)wb_id{
    _wb_id = wb_id;
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    self.view = [[UIView alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    NSMutableArray *controllers  = [NSMutableArray array];
    /*
    UIStoryboard *stryBoard=[UIStoryboard storyboardWithName:@"Second" bundle:nil];
    SecondViewController *secondView = [stryBoard instantiateInitialViewController];
    secondView.ID = _wb_id;
    [controllers addObject:secondView];
     */
    UIStoryboard *storyBoard = [UIStoryboard storyboardWithName:@"WBStoryboard" bundle:nil];
    WBViewController *wbView = [storyBoard instantiateInitialViewController];
    wbView.wb_id = _wb_id;
    [controllers addObject:wbView];
    tabBarController = [[UITabBarController alloc] init];
    tabBarController.viewControllers = controllers;
    tabBarController.customizableViewControllers = controllers;
    tabBarController.delegate = self;
    [self.view addSubview: tabBarController.view];
    // Do any additional setup after loading the view from its nib.
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

@end
